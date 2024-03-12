// scripts/deploy.js
const { ethers } = require("hardhat");
const abi = require("../artifacts/contracts/verifier.sol/Verifier.json");
const proof = require("../../zkArgmax/proof.json");

// const provider2 = new ethers.providers.JsonRpcProvider(`http://127.0.0.1:8545`)

const hrdhatAccountPrivate =
  "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"; //owner
const hrdhatAccountPublic = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"; //owner

async function main() {
  const [deployer, address1] = await ethers.getSigners();
  const BN256G2 = await ethers.getContractFactory("BN256G2");
  const bn256G2 = await BN256G2.deploy();

  const Verifier = await ethers.getContractFactory("Verifier", {
    libraries: {
      BN256G2: bn256G2.target,
    },
  });
  // const gasPrice = ethers.utils.parseUnits('50', 'gwei'); 
  const verifier = await Verifier.deploy();

  console.log("Verifier deployed to:", verifier.target);

  // const x = await verifier
  //   .connect(address1)
  //   .verifyTx(proof.proof, proof.inputs);
  // console.log("YOUR OUTPUT IS: ", x);

  // deployed address 0x057cD3082EfED32d5C907801BF3628B27D88fD80
}
// npx hardhat node --fork https://eth-sepolia.g.alchemy.com/v2/W5EQbGF7eTTgGG4nuWgkga0_p5VIkMbZ

//npx hardhat run scripts/deploy.js --network localhost

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
