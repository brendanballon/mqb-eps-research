# Cross flashing

The firmware FL_3Q0909144JH1_5063.odx is compatible with following racks according to the ODX flash file, other firmwares may be compatible however this hasn't been tested yet.

| Part Number |
3Q0909144C
3Q0909144D
3Q0909144E
3Q0909144F
3Q0909144G
3Q0909144L
3Q0909144H
5Q0909144B
5Q0909144B
5Q0909144F
5Q0909144F
5Q0909144G
5Q0909144H
5Q0909144K
5Q0909144L
5Q0909144M
5Q0909144N
5Q0909144P
5Q0909144Q
5Q0909144R
5Q0909144S
5QD909144S
3Q0909144J
5Q0909144YA
5Q0909144YB
5Q0909144YC
5Q0909144YD
5Q0909144YE
5Q0909144YF
5Q0909144YG
5Q0909144YH
5Q0909144YI
5Q0909144YJ
5Q0909144YK
5Q0909144YL
5Q0909144YM
5Q0909144ZZ



# Workflow

1. Take your desired .frf file (original update files)
2. Install setup_frf_decoder.exe (located in tools > SGO FRF tools)
3. Run the .frf file thru the decoder. It will probably crash but output the decoded .odx file in its install directory.
3. Open the .odx files in a text editor of your choice.
You'll see some long strings of hex code in <FLASHDATAS>.
/UNVERIFIED You'll want to aim for the longest one, usually labelled DATA or something similar, this should be the main part of the FW.
4. Copy the hex string.
5. Open WinHex (again, full unlocked portable version is in tools folder)
6. Paste the copied code as hex (otherwise it pastes as regular unicode and translates it as unicode text)
7. Save the result
8. Open in ghidra

# Notes

this is fw from 5Q0 909 144 R.



i have successfully localized security access codes on this MQB EPS. in this case, they seem to start at 00048a20 in format:
2 bytes security code followed by
2 bytes 00 followed by
1 byte incrementing - starting at 01 with the first code, followed by 02, 04, 08 and 10 for the next codes. followed by
3 bytes 00



the known codes were 28183 (coding), 44595 and 19249 (adaptation), which were all successfully found in the fw. unknown codes that i've found are 44922 and 21230. i haven't actually tested any of these unknown codes yet.