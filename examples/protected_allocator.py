# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
from dataclasses import dataclass


@gl.contract_interface
class ICommonCause:
    class View:
        def is_admitted(self, commitment_id: u256, expected_mapping_hash: str) -> bool: ...
        def get_commitment(self, commitment_id: u256) -> dict: ...
    class Write:
        pass


@allow_storage
@dataclass
class Allocation:
    allocation_id: u256
    commitment_id: u256
    mapping_hash: str
    action_hash: str
    executor: Address


class ProtectedAllocator(gl.Contract):
    """Tiny consumer proving that CommonCause admission can gate another IC."""

    owner: Address
    commoncause_address: Address
    riskbook_id: u256
    allocations: TreeMap[u256, Allocation]
    consumed_actions: TreeMap[str, bool]
    next_allocation_id: u256

    def __init__(self, commoncause_address: Address, riskbook_id: u256):
        self.owner = gl.message.sender_address
        self.commoncause_address = commoncause_address
        self.riskbook_id = riskbook_id
        self.next_allocation_id = u256(1)

    @gl.public.write
    def execute(self, commitment_id: u256, expected_mapping_hash: str, action_hash: str) -> u256:
        action_hash = str(action_hash).lower()
        if len(action_hash) != 64 or any(char not in "0123456789abcdef" for char in action_hash):
            raise gl.vm.UserError("EXPECTED: action_hash must be a 64-character hex digest")
        if self.consumed_actions.get(action_hash, False):
            raise gl.vm.UserError("EXPECTED: action already consumed")
        commoncause = ICommonCause(self.commoncause_address)
        commitment = commoncause.view().get_commitment(commitment_id)
        if int(commitment["riskbook_id"]) != int(self.riskbook_id):
            raise gl.vm.UserError("EXPECTED: commitment belongs to another risk book")
        if not commoncause.view().is_admitted(commitment_id, expected_mapping_hash):
            raise gl.vm.UserError("EXPECTED: CommonCause commitment is not admitted")
        allocation_id = self.next_allocation_id
        self.next_allocation_id = u256(int(self.next_allocation_id) + 1)
        allocation = self.allocations.get_or_insert_default(allocation_id)
        allocation.allocation_id = allocation_id
        allocation.commitment_id = commitment_id
        allocation.mapping_hash = str(expected_mapping_hash)
        allocation.action_hash = action_hash
        allocation.executor = gl.message.sender_address
        self.consumed_actions[action_hash] = True
        return allocation_id

    @gl.public.view
    def get_allocation(self, allocation_id: u256) -> dict:
        allocation = self.allocations.get(allocation_id)
        if allocation is None:
            raise gl.vm.UserError("EXPECTED: unknown allocation")
        return {
            "allocation_id": int(allocation.allocation_id),
            "commitment_id": int(allocation.commitment_id),
            "mapping_hash": str(allocation.mapping_hash),
            "action_hash": str(allocation.action_hash),
            "executor": str(allocation.executor),
        }
