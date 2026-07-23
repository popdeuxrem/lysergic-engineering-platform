# MM0.1 Metamodel Taxonomy
Status: Accepted Baseline Normative  
Version: 0.1.0

The Engineering Control Plane (ECP) metamodel enforces a strict separation
between structural components, graph edges, and stateful entities.

## Structural Primitive (L0)

Immutable value objects.  
Characteristics:  
- no lifecycle  
- no graph edges  
- deterministic serialization  

Examples:  
- Identity  
- Reference  
- Version  
- MetadataFragment

## Relationship Primitive (L1)

Graph edge definitions.  
Characteristics:  
- directional  
- owns edge semantics  
- defines cardinality  
- maps to predicates  

Examples:  
- OwnershipBinding  
- DependencyBinding  
- CapabilityBinding

## Entity Primitive (L2)

First-class graph nodes.  
Characteristics:  
- identity  
- lifecycle  
- state transitions  

Examples:  
- Artifact  
- Capability  
- Scope  
- AuthorityContract
