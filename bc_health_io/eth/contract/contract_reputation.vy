# @title Smart Reputation
# @author catedt
# @notice This is a Smart Reputation.

ISSUED: constant(uint256) = 100
HAS_REPUTATION: constant(uint256) = 101
CLOSED: constant(uint256) = 102

struct Doctor:
  doctor_id: address
  email: string[100]
  repute: int128
  repute_count: int128
  p_center_score: int128
  date_created: timestamp
  date_updated: timestamp
  status: uint256

Transfer: event({_from: indexed(address), _to: indexed(address), _status: uint256})

doctors: map(address, Doctor)
mediator: address
date_launched: public(timestamp)


@public
def __init__(_date_launched: timestamp):
    self.date_launched = _date_launched
    self.mediator = msg.sender


@public
@payable
def issue_doctor(_address: address, _email: string[100], _date_created: timestamp) -> uint256:
    assert len(_email) != 0

    self.doctors[_address] = Doctor({ doctor_id: _address, email: _email, repute: 0, repute_count:0, p_center_score:0, date_created: _date_created, date_updated: _date_created, status: ISSUED})

    log.Transfer(msg.sender, _address, self.doctors[_address].status)

    return self.doctors[_address].status


@public
@payable
def issue_doctor_repute_center_scoring(_address: address,
                                    _has_check_identity: bool,
                                    _has_career_posting: bool,
                                    _has_post_specialization: bool) -> int128:
    assert self.doctors[_address].status == ISSUED

    score: int128 = 20

    if _has_check_identity:
        score += 10

    if _has_career_posting:
        score += 10

    if _has_post_specialization:
        score += 10

    self.doctors[_address].p_center_score = score
    self.doctors[_address].repute = 100

    self.doctors[_address].status = HAS_REPUTATION

    return self.doctors[_address].p_center_score


@public
@payable
def add_increment_repute_customer_scoring(_address: address,
                                    _complain_count: int128,
                                    _has_not_delay: bool,
                                    _has_regulation_observance: bool ) -> int128:
    assert self.doctors[_address].status == HAS_REPUTATION

    self.doctors[_address].repute_count += 1

    score: int128 = 0
    subtract_point: int128 = 0

    if _complain_count == 0:
        score += 25
        subtract_point = 0
    else:
        subtract_point = -5 * _complain_count

    if _has_not_delay:
        score += 15

    if _has_regulation_observance:
        score += 10

    repute: int128 = self.doctors[_address].repute
    p_center_score:int128 = self.doctors[_address].p_center_score

    repute = (repute + (p_center_score + score - subtract_point)) / 2

    self.doctors[_address].repute_count += 1
    self.doctors[_address].repute = repute
    return self.doctors[_address].repute


@public
@payable
def set_status_issued_doctor(_address: address):
    self.doctors[_address].status = ISSUED


@public
@payable
def set_status_doctor_has_reputation(_address: address):
    self.doctors[_address].status = HAS_REPUTATION


@public
@payable
def set_status_doctor_closed(_address: address):
    self.doctors[_address].status = CLOSED


@public
@constant
def issued_doctor_repute(_address: address) -> int128:
    return self.doctors[_address].repute


@public
@constant
def get_p_center_score(_address: address) -> int128:
    return self.doctors[_address].p_center_score


@public
@constant
def issued_doctor_state(_address: address) -> uint256:
    return self.doctors[_address].status


@public
@constant
def get_mediator() -> address:
    return self.mediator