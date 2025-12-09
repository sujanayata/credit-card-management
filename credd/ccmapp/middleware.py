class CreditCardMaskMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        # Only modify POST requests
        if request.method == "POST":
            cc_num = request.POST.get("cc_num")

            if cc_num:
                # Remove spaces/dashes
                cleaned = cc_num.replace(" ", "").replace("-", "")

                # Mask logic: XXXX-XXXX-XXXX-1234
                last4 = cleaned[-4:]
                masked = f"XXXX-XXXX-XXXX-{last4}"

                # Inject masked number back into request
                # request.POST is immutable, so we copy it:
                data = request.POST.copy()
                data["cc_num"] = masked
                request.POST = data

        response = self.get_response(request)
        return response