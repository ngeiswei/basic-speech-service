import sys
import logging

import grpc
import concurrent.futures as futures

import service.common


# Importing the generated codes from buildproto.sh
import service.service_spec.basic_pitch_service_pb2_grpc as grpc_bt_grpc
from service.service_spec.basic_pitch_service_pb2 import Output

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("basic_pitch_service")


"""
Basic Pitch service from Spotify to convert audio to MIDI.
"""


# Create a class to be added to the gRPC server
# derived from the protobuf codes.
class BasicPitchServicer(grpc_bt_grpc.BasicPitch):
    def __init__(self):
        self.audio_file = None
        self.output = None
        # Just for debugging purpose.
        log.debug("BasicPitchServicer created")

    # The method that will be exposed to the snet-cli call command.
    # request: incoming data
    # context: object that provides RPC-specific information (timeout, etc).
    def audio2midi(self, request, context): # NEXT: add type annotations
        # In our case, request is an Input() object (from .proto file)
        self.audio_file = request.audio_file

        # To respond we need to create an Output() object (from .proto file)
        self.output = Output()

        self.output.midi_file = None # NEXT
        log.debug("audio2midi({})={}".format(self.audio_file, self.output.midi_file))
        return self.output


# The gRPC serve function.
#
# Params:
# max_workers: pool of threads to execute calls asynchronously
# port: gRPC server port
#
# Add all your classes to the server here.
# (from generated .py files by protobuf compiler)
def serve(max_workers=10, port=7777):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    grpc_bt_grpc.add_BasicPitchServicer_to_server(BasicPitchServicer(), server)
    server.add_insecure_port("[::]:{}".format(port))
    return server


if __name__ == "__main__":
    """
    Runs the gRPC server to communicate with the Snet Daemon.
    """
    parser = service.common.common_parser(__file__)
    args = parser.parse_args(sys.argv[1:])
    service.common.main_loop(serve, args)
