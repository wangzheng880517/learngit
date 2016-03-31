# -*- coding: utf-8 -*-
import os
import sys
import re
import _winreg

#从regedit中获取netbrain ES安装目录
def regedit_find():
	i=0
	s=[]
	try:
		#判断系统是64位的
	    if sys.version.find("64 bit")!=-1:
	        
	        key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"software\Wow6432Node\NetBrain\NetBrain Enterprise Server\WebServer")
	        while 1:
	            value=_winreg.EnumValue(key,i)
	            if str(value[1]).find("NetBrain")!=-1:
	                s.append(value[1])
	                return s

	            i+=1
	    #判断系统是32位的
	    else:
	        key=_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,r"software\NetBrain\NetBrain Enterprise Server\WebServer")
	        while 1:
	            
	            value=_winreg.EnumValue(key,i)
	            if str(value[1]).find("NetBrain")!=-1:
	                s.append(value[1])
	                return s
	            i+=1
	    
	except WindowsError:
	    print

#从文件中获取关键字行与内容
def search_log(path, *args):
	n=0
	result_path=r"c:\result.log"
	if os.path.exists(result_path):
		result=open(result_path,"a")
	else:
		result=open(r"c:\result.log","a")
	if os.path.exists(path):
		#path路径是一个文件
		if os.path.isfile(path):
			dmp=path.split("\\")[-1].split(".")
			#print dmp
	
			if "dmp" in dmp:
				print path
			
			else:
				ff=open(path,"r")	
				lines=ff.readlines()
				#list 转换字符串，用来查到关键，如没有关键字，该路径不会输出到result.log 文件夹中
				content="".join(lines)
				for wording in args:
					if content.lower().find(wording) >- 1:
						path_file="log path:"+ path + "\r\n"
						result.write("+"*100+"\n")
						result.write(path_file)	
						#result.write("\r\n"*2)
						for line in lines:
							n+=1
							if line.lower().find(wording) > -1:
								output="line:%s %s"%(str(n),line.strip("\r\n")) +"\r\n"
								result.write(output)
						result.write("+"*100+"\n")
						result.write("\r\n")		
				ff.close()
		#path路径是一个目录
		elif os.path.isdir(path):
			for log in os.listdir(path):
				if log.find("nbwsEx") > -1:
					if os.path.isdir(os.path.join(path,log)):
						nbwsEx_path=os.path.join(path,log)
						result.write("*"*100+"\n")
						result.write("bwsEx  directory exist and have files:\n")
						result.write(nbwsEx_path+"\n")
						result.write("--------------\n")
						for nbwsEx_file in os.listdir(nbwsEx_path):							
							result.write(os.path.join(nbwsEx_path,nbwsEx_file) + "\n")
						result.write("*"*100 + "\n")		
					else:
						continue	

				log_z=log.split(".")
				#查找是log后缀名的文件，如xx.log,xx.log.1
				for log_word in log_z:
					if log_word == "log":
						path_full=os.path.join(path,log)
					
						ff=open(path_full,"r")
						lines=ff.readlines()
						content="".join(lines)
						for wording in args:
							if content.lower().find(wording) > -1:
								result.write("+"*100+"\n")
								result.write("log path:%s\r\n" % path_full)
								#result.write("\r\n"*2)

								for line in lines:
									n+=1
									if line.lower().find(wording) > -1:

										output="line:%s %s"%(str(n),line.strip("\r\n")) +"\r\n"
										result.write(output)
								result.write("+"*100+"\n")
								result.write("\r\n"*2)		
		
						ff.close()
					elif log_word=="dmp":

						print "have a dmp file,Name:%s"%log


		else:
			print " "
		
	result.close()			


		
#获得ES,EE,NS,AS所有log目录下文件路径
def path_Serach():

	#path_list=[]
	workpaces=[]
	#调用regedit_find()函数，获取Netbrain安装路径
	s=regedit_find() 
	if s !=None and len(s)>0:
		#拼接EE端log文件夹路径
		EE_Log=os.path.join(s[0],r"Workstation Enterprise Edition\log")
		#拼接OE端log文件夹路径
		OE_log=os.path.join(s[0],r"Workstation Operator Edition")
		#拼接NS端log文件夹路径
		NS_log=os.path.join(s[0],r"Network Server\log")
		#拼接AS端 disovery log 文件夹路径
		AS_dis_log=os.path.join(s[0],r"autoserver\NetBrain Discovery\log")
		#拼接AS端Gateway log文件夹路径
		AS_Gate_log=os.path.join(s[0],r"autoserver\NetBrain Gate\log")
		#拼接AS端search log 文件夹路径
		As_search_log=os.path.join(s[0],r"autoserver\NetBrain Gate\log")
		#拼接ES端license log文件夹路径
		ES_license_log=os.path.join(s[0],r"Enterprise Server\License Server\log")
		#拼接ES端Workspace server log 文件夹路径
		ES_WServer_log=os.path.join(s[0],r"Enterprise Server\Workspace Server\log")
		#拼接ES端workpace 文件夹路径，由于workspace有几个是不确定的，所以下面的代码有特殊的出处理
		ES_workspace_log=os.path.join(s[0],r"Enterprise Server\Workspaces")
		#
		#使用FileExist function获取所有log文件夹
		path_list=FileExist(EE_Log,OE_log,NS_log,AS_dis_log,AS_Gate_log,As_search_log,ES_license_log,ES_WServer_log)
		
		#获取worksapce中log 文件，由于workspce不能确定有几个，所有要单独处理
		if os.path.exists(ES_workspace_log):
			#获取该server中有几个workspace 文件夹 		
			for Workspace in os.listdir(ES_workspace_log):

				path_half=Workspace+ "\\WebServer\\log"
				path_full=os.path.join(ES_workspace_log,path_half)
				workpaces.append(path_full)

			#获取所有workpace log文件
			for workspace in workpaces:
				for log  in os.listdir(workspace):
					path=os.path.join(workspace,log)
					if os.path.isfile(path):
						path_list.append(path)

		return path_list

	else:
		print "don't find path in regedit,"

#获取Netbrain log文件夹函数
def FileExist(*args):
    path_s = []
    for path in args:
        if os.path.exists(path):
        	for path,dirs,files in os.walk(path):
        		for fileName in files:
        			path_s.append(os.path.join(path,fileName))
        		for dirName in dirs:
        			if dirName == "nbwsEx":

        				if len(os.listdir(os.path.join(path,dirName))) > 0:
        					path_result=r"c:/result.log"
        					ff=open(path_result,"w")
        					ff.write("*"*100 +"\n")
        					ff.write("bwsEx  directory exist and have files:\n")
        					ff.write(os.path.join(path,dirName) + "\n")
        					ff.write("-------------------\n")
        					for nbwsExfile in os.listdir(os.path.join(path,dirName)):                        
						        if os.path.exists(path_result):
						            ff.write(os.path.join(os.path.join(path,dirName),nbwsExfile)+"\n")
						#print "nbwsEx  directory exist and have files:%s"%os.path.join(os.path.join(path,dirName),nbwsExfile)
        					ff.write("*"*100 +"\n")	
        					ff.close()
        				else:
        					print "nbwsEx  directory exist and have no file:%s"%os.path.join(path,dirName)
        			else:
        				continue



        else:
            print "%s dir dose not exist!!!" %path
    if len(path_s) >0:
        return path_s
    else:
        return None
#每次running，都需要清空result.log
def ClearResult():
	path_result=r"c:/result.log"
	if os.path.exists(path_result):
		ff=open(path_result,"w")
		ff.close()			

#查找server端所有log中，带有关键字的log会输出到result.log文件夹中
def FindAllLog():
	nbwsEx=False
	path_list=path_Serach()
	if path_list !=None:
		for path in path_list:
			
			search_log(path,"failed","error","crash","time out")
	
if __name__ == '__main__':
	#clear result
	ClearResult()
	#查找EE，ES ，AS，NS 所有log，结果显示result.log中
	#FindAllLog()
	#path_Serach()
	#test 网络路径
	'''path_s=r"\\10.10.10.6\Share Doc\User\wangzheng\57464"
	search_log(path_s,"error")'''


	path=r"C:\Program Files (x86)\NetBrain\Workstation Enterprise Edition\log"
	search_log(path,"error")

