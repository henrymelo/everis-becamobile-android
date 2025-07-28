
import os

MODULE_TYPE = input("Tipo de módulo (feature/core): ").strip().lower()
MODULE_NAME = input("Nome do módulo (ex.: payments ou analytics): ").strip()

if MODULE_TYPE not in ["feature", "core"]:
    print("❌ Tipo inválido. Use 'feature' ou 'core'.")
    exit(1)

module_path = f"{MODULE_TYPE}/{MODULE_NAME}"
sample_path = f"{MODULE_TYPE}/{MODULE_NAME}-sample" if MODULE_TYPE == "feature" else None

# Criar diretório principal e de testes
os.makedirs(module_path, exist_ok=True)
test_dir = f"{module_path}/src/test/java/com/example/{MODULE_NAME}"
os.makedirs(test_dir, exist_ok=True)

# build.gradle para módulo principal
module_gradle = f"""
plugins {{
    id 'com.android.library'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    compileSdk 34
}}

dependencies {{
    {"implementation project(\":core:networking\")" if MODULE_TYPE == "feature" else ""}
    implementation project(":core:ui")
    testImplementation "junit:junit:4.13.2"
}}
"""
with open(f"{module_path}/build.gradle", "w") as f:
    f.write(module_gradle)

# Criar teste unitário inicial
test_file = f"""
package com.example.{MODULE_NAME}

import org.junit.Assert.assertTrue
import org.junit.Test

class ExampleUnitTest {{
    @Test
    fun sampleTest() {{
        assertTrue("Teste básico do módulo {MODULE_NAME}", true)
    }}
}}
"""
with open(f"{test_dir}/ExampleUnitTest.kt", "w") as f:
    f.write(test_file)

# Criar sample se for feature
if MODULE_TYPE == "feature":
    os.makedirs(sample_path, exist_ok=True)
    sample_gradle = f"""
plugins {{
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}}

android {{
    compileSdk 34

    defaultConfig {{
        applicationId "com.example.{MODULE_NAME}.sample"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }}
}}

dependencies {{
    implementation project(":feature:{MODULE_NAME}")
}}
"""
    with open(f"{sample_path}/build.gradle", "w") as f:
        f.write(sample_gradle)

# Atualizar settings.gradle
settings_path = "settings.gradle"
if os.path.exists(settings_path):
    with open(settings_path, "a") as f:
        f.write(f'\ninclude(":{MODULE_TYPE}:{MODULE_NAME}")\n')
        if MODULE_TYPE == "feature":
            f.write(f'include(":{MODULE_TYPE}:{MODULE_NAME}-sample")\n')

print(f"✅ Módulo {MODULE_TYPE}:{MODULE_NAME} criado com sucesso com teste inicial!")
