from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from json import loads

from .models import User

def validate_pair_names_input_object(key: str, body: dict[str, object]) -> HttpResponse:
	if key not in body:
		return HttpResponseBadRequest(f"there's no {key!r} key")
	list_of_names = body[key]
	if not isinstance(list_of_names, list):
		return HttpResponseBadRequest(f"{key!r} doesn't contain a list of names")
	for elem in list_of_names:
		if not isinstance(elem, list):
			return HttpResponseBadRequest(f"an element in a list {key!r} isn't a list itself")
		if len(elem) != 2:
			return HttpResponseBadRequest(f"an element in a list {key!r} isn't a list with exactly two elements")
		if not isinstance(elem[0], str) or len(elem[0]) == 0:
			return HttpResponseBadRequest(f"the name in an element isn't a non-empty string")
		if not isinstance(elem[1], str) or len(elem[1]) == 0:
			return HttpResponseBadRequest(f"the ID in an element isn't a non-empty string")
	return None

def validate_pair_names_input(body: dict[str, object]) -> HttpResponse:
	if (err := validate_pair_names_input_object("first_names", body)) != None:
		return err
	if (err := validate_pair_names_input_object("last_names", body)) != None:
		return err
	return None

@require_POST
def pair_names(request: HttpRequest) -> HttpResponse:
	if request.content_type != "application/json":
		return HttpResponseBadRequest("the content type isn't application/json")
	
	try:
		parsed = loads(request.body)
	except:
		return HttpResponseBadRequest("can't parse the given json document")
	
	if (err := validate_pair_names_input(parsed)) != None:
		return err

	partial_full_names: dict[str, User] = dict()
	for pair in parsed["first_names"]:
		id, first_name = pair[1], pair[0]
		partial_full_names[id] = User(first_name, "")
	for pair in parsed["last_names"]:
		id, last_name = pair[1], pair[0]
		if id not in partial_full_names:
			partial_full_names[id] = User("", last_name)
		else:
			partial_full_names[id].last_name = last_name
	
	full_names_list, unpaired_list = [], []
	for id, user in partial_full_names.items():
		if user.first_name == "" or user.last_name == "":
			unpaired_list.append([user.first_name, user.last_name, id])
		else:
			full_names_list.append([user.first_name, user.last_name, id])
	full_names_list.sort(key=lambda e: e[2])
	unpaired_list.sort(key=lambda e: e[2])
	
	return JsonResponse({"full_names": full_names_list, "unpaired": unpaired_list})
