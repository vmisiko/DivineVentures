from divineVentures.mpesa import keys
import base64

def generate_password(formated_time):

    data_to_encode = keys.bussiness_shortcode + keys.lipa_na_mpesa_pass_key + formated_time
    encode_string = base64.b64encode(data_to_encode.encode())
    # print(encode_string, "this is encoded string")
    decoded_password = encode_string.decode("utf-8")

    return decoded_password