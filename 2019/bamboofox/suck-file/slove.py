import zipfile


fname = "a79cc81251ba4c66ed91ccd01b423598818a76cf"

while True:
    data = open(fname,'rb').read()
    open(fname, "wb").write("PK" + data[2:])
    z = zipfile.ZipFile(fname)
    fname = z.namelist()[0]
    print fname
    if fname == 'flag' :
	open(fname, "wb").write("BA" + data[2:])
	break
    z.extractall()
