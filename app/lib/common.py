from rest_framework.views import APIView
# from app.lib.response import ApiResponse
# from app.users.views import UserProfile
# from Winalytics.apps.approach.models import Approach
from rest_framework.authtoken.models import Token
from django.views.generic.edit import UpdateView
# import itertools
# import operator


class AccessUserObj:

	def fromToken(self,request):
		token = request.META['HTTP_AUTHORIZATION'].replace("Token","")	
		return Token.objects.get(key=str(token).strip())

# class PostCommonMethods:

# 	def getCreatedByName(obj):
# 		try:
			
# 			userProfile = UserProfile.objects.get(user_id = obj.created_by)
			
# 			return userProfile.fname
# 		except Exception as err:
# 			print(err)
# 			return None	

# class PhaseLib:

# 	def CheckPhaseExist(self, request, args):
# 		try:
# 			phase = Phase.objects.filter(**args).get(id=request.data.get('phase'))
# 			print(phase.id)
# 			if int(phase.id) is None:
# 				return True
# 			return False
# 		except Exception as err:
# 			print(err)
# 			return True	

class RequestOverwrite(UpdateView):

	def overWriteUserId(self, request, dic):
		try:
			if request.POST._mutable is False:
				request.POST._mutable = True
			
			for key,value in dic.items():
				request.POST[key] = value
		except Exception as err:
			print(err)
			return False

	def overWrite(self, request, dic):
		try:
			try:
				if request.data._mutable is False:
					request.data._mutable = True
			except:
				pass
			for key,value in dic.items():
				request.data[key] = value
		except Exception as err:
			print(err)
			return False

# class CheckExistance():
# 	def isExists(self,Object,filter):
# 		obj = Object.objects.filter(**filter)

# 		if obj.exists():
# 			return True
# 		return False			


# class Common():
# 	def most_common(self, L):
# 	  # get an iterable of (item, iterable) pairs
# 	  SL = sorted((x, i) for i, x in enumerate(L))
# 	  # print 'SL:', SL
# 	  groups = itertools.groupby(SL, key=operator.itemgetter(0))
# 	  # auxiliary function to get "quality" for an item
# 	  def _auxfun(g):
# 	    item, iterable = g
# 	    count = 0
# 	    min_index = len(L)
# 	    for _, where in iterable:
# 	      count += 1
# 	      min_index = min(min_index, where)
# 	    # print 'item %r, count %r, minind %r' % (item, count, min_index)
# 	    return count, -min_index
# 	  # pick the highest-count/earliest item
# 	  return max(groups, key=_auxfun)[0]
