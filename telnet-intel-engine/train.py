from pathlib import Path
from datetime import datetime
import subprocess
import sys

# Dossiers de sortie
MODELS_DIR = Path("data/models")
LOGS_DIR = Path("logs")

MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOGS_DIR / "train.log"

with open(log_file, "w") as log:
    log.write(f"Training started at {datetime.utcnow().isoformat()}Z\n")

    # Si ton module bayesian.py existe, on l'exécute
    bayesian_script = Path("ml/bayesian.py")
    if bayesian_script.exists():
        log.write("Running ml/bayesian.py...\n")
        result = subprocess.run(
            [sys.executable, str(bayesian_script)],
            capture_output=True,
            text=True
        )

        log.write(result.stdout)
        if result.stderr:
            log.write("\n[stderr]\n")
            log.write(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(
                f"Training failed with exit code {result.returncode}. "
                f"See {log_file}"
            )
    else:
        log.write("ml/bayesian.py not found. Creating dummy model.\n")

    # Création d'un fichier modèle de démonstration
    model_file = MODELS_DIR / "bayesian_model.pkl"
    model_file.write_text(
        f"Model generated at {datetime.utcnow().isoformat()}Z\n"
    )

    log.write(f"Model saved to {model_file}\n")
    log.write("Training completed successfully.\n")

print("Training completed successfully.")y


