import rdkit
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from mordred import Calculator, descriptors
import numpy as np

'Compute Molecular Descriptors (MolDs) from SMILES'
class MordredCalculator(object):
    def __init__(self, smiles):
        self.smiles = smiles

    def calc_mordred(self):
        mols = [Chem.MolFromSmiles(smi) for smi in self.smiles]
        calc = Calculator(descriptors, ignore_3D=True)
        mordred = calc.pandas(mols)
        fps = mordred.to_numpy()
        return fps
    
'Compute Fingerprint Features (FFs) from SMILES'
radius = 3
nBits = 2048
class MorganCalculator(object):
    def __init__(self, smiles):
        self.smiles = smiles
        self.radius = radius
        self.nbits = nBits
        
    def calc_morgan(self):
        fps = []
        mols = [Chem.MolFromSmiles(smi) for smi in self.smiles]
        for mol in mols:
            fps.append(list(rdMolDescriptors.GetHashedMorganFingerprint(mol, radius=self.radius, nBits=self.nbits)))
        return np.array(fps)
    