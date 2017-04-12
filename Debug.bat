@echo off
set param=%1

echo DEBUGGING ONLY
python project/modules/%param:.=/%.py
