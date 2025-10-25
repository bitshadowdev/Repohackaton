from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict

class Action(Enum):
    """Enumerates actions that can be subject to permission checks."""
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    DELETE_FILE = "delete_file"
    EXECUTE_COMMAND = "execute_command"
    API_CALL = "api_call"

@dataclass
class PermissionRequest:
    """Represents a request for a specific action on a resource."""
    agent_id: str
    action: Action
    resource: str
    context: Dict[str, Any] = field(default_factory=dict)

class PermissionsManager:
    """
    A simple, default permissions manager.

    By default, it denies potentially dangerous actions and allows others.
    This class is intended to be extended with more sophisticated logic.
    """
    def __init__(self):
        # More complex rules can be defined here
        self.denied_actions = {
            Action.DELETE_FILE,
        }

    def request_permission(self, request: PermissionRequest) -> bool:
        """
        Evaluates a permission request.

        Args:
            request: The permission request to evaluate.

        Returns:
            True if the action is permitted, False otherwise.
        """
        print(f"Permission request from agent '{request.agent_id}' for action '{request.action.value}' on resource '{request.resource}'.")

        if request.action in self.denied_actions:
            # Simple rule: deny certain action types by default.
            # A real implementation would have more granular checks,
            # e.g., checking the specific resource path.
            if "important" in request.resource:
                 print("-> Decision: DENIED (action is in default deny list).")
                 return False

        print("-> Decision: GRANTED.")
        return True


from commands import Command, CommandResult


class InteractivePermissionsManager:
    """
    A permissions manager that prompts the user for a decision on important actions.
    """
    def __init__(self, important_actions=None):
        if important_actions is None:
            self.important_actions = {
                Action.WRITE_FILE,
                Action.DELETE_FILE,
                Action.EXECUTE_COMMAND
            }
        else:
            self.important_actions = set(important_actions)

    def request_permission_and_execute(self, command: Command) -> CommandResult:
        """
        Evaluates a permission request and executes the command if the user grants permission.

        Args:
            command: The command object to evaluate and execute.

        Returns:
            A CommandResult indicating the outcome.
        """
        request = command.permission_request
        print(f"Permission request from agent '{request.agent_id}' for action '{request.action.value}' on resource '{request.resource}'.")

        if request.action not in self.important_actions:
            print("-> Decision: GRANTED (action is not considered important). Executing...")
            return command.execute()

        # Prompt the user for a decision
        print("\n" + "!"*80)
        print("! IMPORTANT ACTION REQUIRES YOUR APPROVAL")
        print("!"*80)
        print(f"  - Agent:    {request.agent_id}")
        print(f"  - Action:   {request.action.value}")
        print(f"  - Resource: {request.resource}")
        if request.context:
            print(f"  - Context:  {request.context}")
        
        while True:
            try:
                response = input("  > Grant permission and execute? (yes/no): ").lower().strip()
                if response in ["yes", "y"]:
                    print("-> Decision: GRANTED by user. Executing...")
                    return command.execute()
                elif response in ["no", "n"]:
                    print("-> Decision: DENIED by user.")
                    return CommandResult(success=False, message="Execution denied by user.")
                else:
                    print("  > Invalid input. Please enter 'yes' or 'no'.")
            except (EOFError, KeyboardInterrupt):
                print("\n-> Decision: DENIED (no user input received).")
                return CommandResult(success=False, message="Execution denied due to no user input.")
