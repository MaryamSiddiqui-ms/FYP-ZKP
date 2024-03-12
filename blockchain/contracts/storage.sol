// SPDX-License-Identifier: LGPL-3.0-only
// This file is LGPL3 Licensed
pragma solidity ^0.8.0;

contract ProofContract {
    struct G1Point {
        uint X;
        uint Y;
    }

    struct G2Point {
        uint[2] X;
        uint[2] Y;
    }

    struct Proof {
        G1Point a;
        G2Point b;
        G1Point c;
    }

    mapping(bytes32 => Proof) proofs;

    function generateProofId(Proof memory proof) private pure returns (bytes32) {
        return keccak256(abi.encodePacked(proof.a.X, proof.a.Y, proof.b.X, proof.b.Y, proof.c.X, proof.c.Y));
    }

    function storeProof(Proof memory proof) external {
        bytes32 proofId = generateProofId(proof);
        require(proofs[proofId].a.X == 0 && proofs[proofId].a.Y == 0, "Proof already exists"); 

        proofs[proofId] = proof;
    }

    function getProof(bytes32 proofId) external view returns (Proof memory) {
        return proofs[proofId];
    }
}