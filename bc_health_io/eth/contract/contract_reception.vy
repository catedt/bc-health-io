# @title Smart Reception
# @author catedt
# @notice This is a Smart Reception.

value: uint256(wei)
fee: uint256(wei)
mediator: address
receptionist: address
adopter: address

reception_started: bool
adopted: bool
received: bool
confirmed: bool
complained: bool
receive_count: int128


@public
@payable
def __init__(_receptionist: address, _value:uint256(wei), _fee:uint256(wei)):
    assert msg.sender != _receptionist
    self.mediator = msg.sender
    self.receptionist = _receptionist
    self.receive_count = 0
    self.value = _value
    self.fee = _fee


@public
@payable
def reception():
    assert msg.sender == self.receptionist
    assert msg.value == self.value + self.fee

    self.reception_started = True
    send(self.mediator, self.fee)

@public
@payable
def abort():
    assert self.reception_started
    assert msg.sender == self.mediator

    selfdestruct(self.receptionist)


@public
@payable
def adopt_reception():
    assert self.receptionist != msg.sender
    assert self.reception_started
    assert msg.value == self.fee

    self.adopter = msg.sender
    self.adopted = True
    send(self.mediator, msg.value)


@public
@payable
def opinion_received():
    assert self.reception_started and self.adopted
    assert msg.sender == self.adopter

    self.received = True
    self.receive_count += 1


@public
def opinion_complained():
    assert self.reception_started and self.adopted and self.received
    assert msg.sender == self.receptionist

    self.complained = True


@public
@payable
def opinion_confirmed():
    assert self.reception_started and self.adopted and self.received
    assert msg.sender == self.receptionist

    self.confirmed = True
    # send(self.adopter, self.value)
    selfdestruct(self.adopter)


@public
@constant
def get_value()->uint256(wei):
    return self.value


@public
@constant
def get_fee()->uint256(wei):
    return self.fee


@public
@constant
def get_mediator()->address:
    return self.mediator


@public
@constant
def get_receptionist()->address:
    return self.receptionist


@public
@constant
def get_adopter()->address:
    return self.adopter


@public
@constant
def is_reception_started()->bool:
    return self.reception_started


@public
@constant
def is_adopted()->bool:
    return self.adopted


@public
@constant
def is_received()->bool:
    return self.received


@public
@constant
def is_complained()->bool:
    return self.complained


@public
@constant
def is_confirmed()->bool:
    return self.confirmed


@public
@constant
def get_received_count()->int128:
    return self.receive_count

