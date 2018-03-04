from ipykernel.kernelbase import Kernel
import re
import time

wait_re = re.compile("wait (\d+)")


class EchoKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot, on steroids"

    def init_metadata(self, parent):
        self.m = super(EchoKernel, self).init_metadata(parent)
        self.m["parent"] = parent
        return self.m

    def w(self, s):
        stream_content = {'name': 'stdout', 'text': s}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def do_execute(self, code, silent,
                   store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            self.w(code)
            self.w("\nmetadata was %s\n" % self.m)

            m = wait_re.search(code)
            if m:
                self.w("MATCH\n")
                try:
                    delay = int(m.group(1))
                    time.sleep(delay)
                    self.w("waited %d\n" % delay)
                except Exception as e:
                    self.w("wait exception: %s\n" % e)
                self.w("OK matched\n")
            else:
                self.w("NOMATCH\n")


        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}
