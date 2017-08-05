#!/bin/bash
selection=$(zenity --list "Introducir texto" "Extraer texto" "Borrar mensaje en archivo" --column="" --text="Seleccionar" --title="Esteganjalt")
if [ -z "$selection" ]; then 
zenity --warning \
--text="No hay selección o has cancelado.\nEl programa se cerrará"
exit 0
fi
echo $selection
if [[ $selection = "Introducir texto" ]]
then
archivoI=$(zenity --file-selection --title="Selecciona una archivo")
if [ -z "$archivoI" ]; then 
zenity --warning \
--text="Has cancelado.\nEl programa se cerrará"
exit 0
fi
zenity --warning --text "ATENCION\n\nSi el texto a introducir tiene saltos de línea\nponlo primero en un archivo de texto y haz un copia pega"
textoI=$(zenity --entry --title="Entrada mensaje" --text="Introducir texto:" --entry-text "")
if [ "x$textoI" = "x" ]
then
zenity --warning \
--text="No ha introducido texto o ha cancelado\nEl programa se cerrará"
exit 0
fi
#sed -i '$a  comienzo texto:\n'"$textoI"'\n:final texto' "$archivoI"
passE=$(zenity --entry --title="Cifrado" --text="Introducir clave cifrado:" --entry-text "")
if [ "x$passE" = "x" ]
then
zenity --warning \
--text="No ha introducido texto o ha cancelado\nEl programa se cerrará"
exit 0
fi
passE=$(echo "$passE" | tr -d '[[:space:]]')
echo -e "comienzo texto:" >> $archivoI
echo -e "$textoI" | openssl enc -aes-256-cbc -e -a -k $passE >> $archivoI
echo -e ":final texto" >> $archivoI

zenity --info --text="El proceso a finalizado"
exit 0
fi
if [[ $selection = "Extraer texto" ]]
then
archivoE=$(zenity --file-selection --title="Selecciona el archivo a extraer")
if [ -z "$archivoE" ]; then 
zenity --warning \
--text="Has cancelado.\nEl programa se cerrará"
exit 0
fi
textoE=$(zenity --entry --title="Archivo de extracción" --text="Da nombre al archivo donde se extraerá el mensaje\nNo pongas extensión. Será un .txt " --entry-text "")
if [ "x$textoE" = "x" ]
then
zenity --warning \
--text="No ha introducido texto o ha cancelado\nEl programa se cerrará"
exit 0
fi
passD=$(zenity --entry --title="Cifrado" --text="Introducir clave descifrado:" --entry-text "")
if [ "x$passD" = "x" ]
then
zenity --warning \
--text="No ha introducido texto o ha cancelado\nEl programa se cerrará"
exit 0
fi
passD=$(echo "$passD" | tr -d '[[:space:]]')
echo -e  > $textoE.txt
mkdir temporal
archivoT=${archivoE%.*}
archivoT=${archivoT##*/}
echo -e > temporal/$archivoT.txt
awk '/comienzo texto:/,/:final texto/' $archivoE >> temporal/$archivoT.txt
sed -i "1d" temporal/$archivoT.txt
sed -i "1d" temporal/$archivoT.txt
sed -i '$d' temporal/$archivoT.txt
openssl enc -aes-256-cbc -d -a -in temporal/$archivoT.txt -out $textoE.txt -k $passD
rm -rf temporal/
zenity --info --text="El proceso a finalizado"
xdg-open "$textoE.txt"&
sleep 4
exit 0
fi
if [[ $selection = "Borrar mensaje en archivo" ]]
then
archivoB=$(zenity --file-selection --title="Selecciona el archivo que hay que borrar el mensaje")
if [ -z "$archivoB" ]; then 
zenity --warning \
--text="Has cancelado.\nEl programa se cerrará"
exit 0
fi
if ! grep -q "comienzo texto:" "$archivoB";
then
zenity --warning \
--text="Este archivo no contiene mensaje"
exit 0
else
sed -i '/comienzo texto:/,/:final texto/d' $archivoB
zenity --info --text="El mensaje ha sido borrado del archivo"
exit 0
fi
fi
