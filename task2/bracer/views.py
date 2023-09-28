from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from .models import Brace

def check_brace(input: str, brace: Brace) -> int:
	"""
	Checks if the specified brace is balanced in the `input` string.
	Returns 0 if it's balanced or a positive integer specifying how many
	brace symbols are missing.
	"""
	sum = 0
	max_sum = 0
	for i in range(len(input)):
		if input[i] == brace.open:
			sum -= 1
		elif input[i] == brace.close:
			sum += 1
		else:
			continue
		max_sum = max(max_sum, sum)
	unbalanced_count = 2 * max_sum - sum
	return unbalanced_count

@require_POST
def check_braces(request: HttpRequest) -> HttpResponse:
	if request.content_type != "text/plain":
		return HttpResponseBadRequest("the content type isn't text/plain")
	
	braces: list[Brace] = [Brace('(', ')'), Brace('[', ']'), Brace('{', '}')]
	brace_unbalanced_cnt: dict[str, int] = dict()
	for brace in braces:
		missing_count = check_brace(str(request.body), brace)
		if missing_count > 0:
			brace_unbalanced_cnt[brace.open] = missing_count
	if len(brace_unbalanced_cnt.keys()) == 0:
		return HttpResponse()
	msg = ""
	for brace, missing_count in brace_unbalanced_cnt.items():
		msg += f" {brace}: {missing_count},"
	return HttpResponseBadRequest(msg[:len(msg) - 1])
