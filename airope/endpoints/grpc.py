from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost


async def exp():
    host = GrpcWorkerAgentRuntimeHost(address="localhost:50051")
    host.start()
    await host.stop()
