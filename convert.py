import subprocess

latex_file = "./tex/main.tex"
pdf_file = "output.pdf"

# Компилируем LaTeX файл в PDF
subprocess.run(["pdflatex", latex_file])

# Перемещаем файлы и удаляем временные файлы
subprocess.run(["mv", "main.pdf", pdf_file])
subprocess.run(["rm", "main.aux", "main.log"])
