"""Restore the saved core adapters and rebuild the original SFT reference.

Usage: python scripts/restore_lab22_checkpoint.py /path/Lab22_checkpoint_100.zip
Requires the lab CUDA/Unsloth environment. Does not retrain either adapter.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def extract_checkpoint(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError(f"Unsafe archive member: {member.filename}")
        z.extractall(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    import unsloth  # must patch before transformers/peft
    import torch
    from lab22 import config as C
    from lab22 import modeling as MD
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU required; no training or restore has run.")
    extract_checkpoint(args.archive, ROOT)
    checkpoint = C.ADAPTERS / "dpo-checkpoints" / "checkpoint-100"
    if not (checkpoint / "adapter_model.safetensors").is_file():
        raise FileNotFoundError("Missing saved DPO weights")
    if not (C.SFT_ADAPTER / "adapter_model.safetensors").is_file():
        raise FileNotFoundError("Missing saved SFT weights")
    model, tokenizer = MD.load_model(C.SFT_ADAPTER)
    model.save_pretrained_merged(str(C.SFT_MERGED), tokenizer, save_method="merged_16bit")
    del model
    MD.cleanup()
    C.DPO_ADAPTER.mkdir(parents=True, exist_ok=True)
    for name in ("adapter_model.safetensors", "adapter_config.json", "trainer_state.json"):
        shutil.copy2(checkpoint / name, C.DPO_ADAPTER / name)
    cfg_path = C.DPO_ADAPTER / "adapter_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["base_model_name_or_path"] = str(C.SFT_MERGED.resolve())
    cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    tokenizer.save_pretrained(str(C.DPO_ADAPTER))
    for folder, filename in ((C.SFT_ADAPTER, "adapter_model.safetensors"),
                             (C.DPO_ADAPTER, "adapter_model.safetensors")):
        p = folder / filename
        print(p.relative_to(ROOT), hashlib.sha256(p.read_bytes()).hexdigest())
    print("Restored saved adapters; rebuilt SFT reference. No retraining.")


if __name__ == "__main__":
    main()
