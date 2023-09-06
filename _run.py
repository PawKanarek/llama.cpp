from subprocess import Popen, PIPE
import time
from datetime import datetime
import os
import sys

# https://huggingface.co/blog/codellama#conversational-instructions
# <s>[INST] <<SYS>>
# {{ system_prompt }}
# <</SYS>>

# {{ user_msg_1 }} [/INST] {{ model_answer_1 }} </s><s>[INST] {{ user_msg_2 }} [/INST]
s_b = '<s>'
s_e = '</s>'
SYS_b = '<<SYS>>'
SYS_e = '<</SYS>>'
INST_b = '[INST]'
INST_e = '[/INST]'
sys_prompt = "Write code only in python"
# with open("llama_cpp_ref.py", "r") as file: 
#     file = "\n".join(file.readlines())
#prompt = 'def read_process_output():\n\t"""Creates new process of executable unix file main.sh, and continously reads output"""'
prompt_init = """Please write continuation to this code:
```
def read_process_output():
    print("Starting process")
    args = ['./main', 
            '-m', './models/CodeLlama-34b-Instruct/ggml-model-q4_0.gguf',
            '-n', '-1',
            '-c', '4096',
            '-p', prompt]
    continously_read_subprocess(args)
```
"""
prompt_resp ="""The continously_read_subprocess definition is missing. Below is implementation: 
```
from subprocess import Popen, PIPE

def continously_read_subprocess(args: []):
    with Popen(args, stdout=PIPE, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
        save_session(p)
```
"""
new_prompt = """
write function that compares last opened session with current output
"""
#prompt = f'{s_b}{INST_b}\n{sys_prompt.strip()}\n{SYS_e}\\n{prompt_init.strip()}\n{INST_e}'
prompt  = f"<<SYS>>\\n{sys_prompt}\\n<</SYS>>\\n\\n{prompt_init}"
prompt  = f"<s>[INST] {prompt.strip()} [/INST] {prompt_resp.strip()} </s>"
prompt += f"<s>[INST] {new_prompt.strip()} [/INST]"


def read_process_output():
    print("Starting process")
    args = ['./main', 
            '-m', './models/CodeLlama-34b-Instruct/ggml-model-q4_0.gguf',
            '-n', '-1',
            '-c', '4096',
            '-p', prompt]
    continously_read_subprocess(args)
   
def continously_read_subprocess(args: []):
    with Popen(args, stdout=PIPE, universal_newlines=True) as p:
        with open('./_current.txt', 'w') as f:
            for line in p.stdout:
                print(line, end='')
                f.write(line)

def save_session(p):
    with open('./current_session.txt', 'w') as f:
        for line in p.stdout:
            f.write(line)

def main():
    read_process_output()
if __name__ == "__main__":
    main()