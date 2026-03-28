from bioagents.policies.ant import AntPolicy
from bioagents.policies.bee import BeePolicy
from bioagents.policies.default import DefaultPolicy, PlaceholderPolicy


DEFAULT_POLICY_NAME = "default"

POLICY_REGISTRY = {
    "default": DefaultPolicy,
    "ant": AntPolicy,
    "bee": BeePolicy,
    "immune": PlaceholderPolicy,
}


def get_policy(name: str | None = None):
    policy_name = name or DEFAULT_POLICY_NAME
    if policy_name not in POLICY_REGISTRY:
        raise ValueError(f"Unknown policy: {policy_name}")
    policy = POLICY_REGISTRY[policy_name]()
    if policy_name != "default":
        policy.name = policy_name
    return policy
