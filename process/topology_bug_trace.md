# Topology Bug Trace — check_orientability

**Date:** May 2026  
**Module:** `ckm_topology_module.py`  
**Function:** `check_orientability`

---

## Symptom

First run of topology module on K4 (complete graph on 4 nodes — tetrahedron boundary):

```
Expected: H0=1 H1=0 H2=1  orientable (cilindro)
Got:      H0=1 H1=0 H2=1  Möbius(6) — false positive
```

K4 is provably orientable. Its boundary is a 2-sphere. The result was wrong.

C5 (5-cycle) gave correct result: H0=1 H1=1 H2=0 cilindro.

---

## Root cause

`check_orientability` determines whether two adjacent triangles have compatible orientations by checking the sign of their shared edge. The original code used membership:

```python
# Original — WRONG
edges1 = [(i,j),(j,k),(i,k)]
if (a,b) in edges1:
    sign = +1
else:
    sign = -1
```

**Bug:** The boundary formula ∂(i,j,k) = +(j,k) − (i,k) + (i,j) assigns sign −1 to edge (i,k). But membership check returned +1 for all edges in the list — including (i,k).

For K4 triangles stored as (i,j,k) with i<j<k, edge (i,k) always appears as a member → always gets sign +1 → all triangle pairs appear incompatible → false Möbius detection.

---

## Trace

Triangles of K4: (0,1,2), (0,1,3), (0,2,3), (1,2,3)

Pair T0=(0,1,2) and T1=(0,1,3), shared edge (0,1):
- Correct signs: T0→(0,1) is (i,j) → +1; T1→(0,1) is (i,j) → +1
- Same sign → incompatible → should mark as conflict... but wait
- (0,1) is (i,j) in both → sign +1 in both → product = +1 → NOT compatible

Pair T0=(0,1,2) and T2=(0,2,3), shared edge (0,2):
- T0→(0,2) is (i,k) → correct sign = −1
- T2→(0,2) is (i,j) → correct sign = +1
- Product = −1 → compatible ✓

Original code returned +1 for (0,2) in T0 (membership check), making it appear incompatible.

---

## Fix

Replace membership check with boundary formula:

```python
# Fixed — uses boundary formula directly
def _edge_sign(tri, a, b):
    i, j, k = tri
    if (a, b) == (i, j) or (a, b) == (j, k):
        return +1
    elif (a, b) == (i, k):
        return -1
    return None

sign1 = _edge_sign(tri1, a, b)
sign2 = _edge_sign(tri2, a, b)
return +1 if (sign1 * sign2 == -1) else -1
```

---

## Verification

| Graph | Expected | Before fix | After fix |
|-------|----------|-----------|-----------|
| K4 | cilindro | Möbius(6) — false positive | cilindro ✓ |
| C5 | cilindro | cilindro ✓ | cilindro ✓ |
| CKM corpus N=32 | — | cilindro (correct by coincidence) | cilindro ✓ (correct by algorithm) |

The CKM corpus result was correct before the fix — but for the wrong reason. Now it is correct because the algorithm is correct.

---

## Significance

This bug would have produced false Möbius detections on any orientable simplicial complex where edge (i,k) appears in a shared position. In CKM terms: it would have incorrectly classified resolvable divergences as structural incommensurabilities (R12). The distinction matters.
