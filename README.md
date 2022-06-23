# Генерация PDF-документа

Пример генерации сложного PDF-документа (таблица умножения - в данном случае) с ипользованием (Lua)LaTeX.

## Докер

```shell
docker build -t multable .
docker run --rm -v $(pwd):/workdir multable --max-number 7 --language SLAVIC
```

(будет создан файл multable.pdf в текущей директории, он будет ПЕРЕЗАПИСАН, если существует!)

## Ресурсы

[Использование poetry & docker] (https://linuxtut.com/en/43efd6d7aa8eccc2b77e/)
https://hub.docker.com/r/blang/latex
https://github.com/matthewfeickert/Docker-Python3-Ubuntu/blob/master/Dockerfile
https://hub.docker.com/r/danteev/texlive/ (взял отсюда рецепт запуска докера)
https://github.com/reitzig/texlive-docker
https://hub.docker.com/r/thomasweise/docker-texlive-full/
https://hub.docker.com/r/claudiugeorgiu/python-texlive
