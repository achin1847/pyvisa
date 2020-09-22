
import visa

rm = visa.ResourceManager()
list_insts = rm.list_resources()

# search instrument and query information
for index, inst in enumerate(list_insts):
	print(inst)
	access_inst = rm.open_resource(rm.list_resources()[index])
	print(access_inst.query('*IDN?'))
	access_inst.close()
