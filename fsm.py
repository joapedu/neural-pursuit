from enum import Enum
from typing import Callable, Optional, Dict, Any


class State(Enum):
    PATROL = "PATROL"
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    RETURN = "RETURN"


class FSM:
    def __init__(self, initial_state: State = State.PATROL):
        self.current_state = initial_state
        self.previous_state: Optional[State] = None
        self.state_handlers: Dict[State, Callable] = {}
        self.transitions: Dict[State, Dict[State, Callable]] = {}
        self.state_data: Dict[State, Any] = {}

    def add_state_handler(self, state: State, handler: Callable):
        self.state_handlers[state] = handler

    def add_transition(self, from_state: State, to_state: State, condition: Callable):
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][to_state] = condition

    def update(self, *args, **kwargs):
        if self.current_state in self.state_handlers:
            self.state_handlers[self.current_state](*args, **kwargs)

        if self.current_state in self.transitions:
            for next_state, condition in self.transitions[self.current_state].items():
                if condition(*args, **kwargs):
                    self.change_state(next_state)
                    break

    def change_state(self, new_state: State):
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state

    def get_state(self) -> State:
        return self.current_state

    def get_previous_state(self) -> Optional[State]:
        return self.previous_state
