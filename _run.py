# https://huggingface.co/blog/codellama

# SAD
# This task is available in the base and instruction variants of the 7B and 13B models.
# It is not available for any of the 34B models or the Python versions.
# FILL_ME = "<FILL_ME>"
# fill_me_example = f'''def remove_non_ascii(s: str) -> str:
#     """{FILL_ME}
#     return result
# '''

# fill_me_example_decoded = fill_me_example.replcae(FILL_ME)



# this is the way to go
# https://huggingface.co/blog/codellama#conversational-instructions
<s>[INST] <<SYS>>
{{ system_prompt }}
<</SYS>>

{{ user_msg_1 }} [/INST] {{ model_answer_1 }} </s><s>[INST] {{ user_msg_2 }} [/INST]


def main():



    if __name__ == "__main__":
        main()