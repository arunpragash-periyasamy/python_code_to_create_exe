import pexpect

try:
    child = pexpect.spawn('echo Hello World', encoding='utf-8')
    child.expect(pexpect.EOF)
    print("Output:", child.before)
except Exception as e:
    print("Error:", str(e))
