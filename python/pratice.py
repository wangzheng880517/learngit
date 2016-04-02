import time
def pratice_map():

	return list(map(lambda x:x*x,[i for i in range(10)]))

#Decoration
def log(text):
	def decorator(func):
		def wrapper(*arg,**kw):
			print("%s-->call %s():"%(text,func.__name__))
			return func(*arg,**kw)

		return wrapper
	return decorator

@log("execute")
def now():
	print time.time()


if __name__ == '__main__':
	now()


