# #!/bin/bash

# 1. 실행 파일 다운로드  https://drive.google.com/file/d/1-8iHTlNlsrqmEfvWYQq00NgQsczAXsty/view?usp=drive_link
gdown --fuzzy https://drive.google.com/file/d/1-8iHTlNlsrqmEfvWYQq00NgQsczAXsty/view?usp=drive_link
mkdir fbxpython
tar -zxvf fbx202032_fbxpythonsdk_linux.tar.gz -C fbxpython
rm fbx202032_fbxpythonsdk_linux.tar.gz

# 2. python library 생성
cd fbxpython
./fbx202032_fbxpythonsdk_linux

# 3. 파이썬 환경으로 옮기기
PIP="$(which pip)"

ENV="${PIP:0:-4}/../"
PACKAGE="lib/python3.7/dist-packages/"

if [ ! -d "$ENV$PACKAGE" ];
then
PACKAGE="lib/python3.7/site-packages/"
fi

cd lib/Python37_x64
mv * "$ENV$PACKAGE"
cd ../../..

# 4. 남은 파일 제거
rm -rf fbxpython
echo "SUCCESS!"