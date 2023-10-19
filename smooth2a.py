import scipy 
import numpy

def smooth2a(matrixIn,Nr,Nc):
    # device = matrixIn.device
    # matrixIn = matrixIn.cpu().numpy()
    [row,col] = matrixIn.shape
    eL = scipy.sparse.spdiags(numpy.ones((2*Nr,row)),numpy.arange(-Nr,Nr),row,row)
    eR = scipy.sparse.spdiags(numpy.ones((2*Nc,col)),numpy.arange(-Nc,Nc),col,col)
    nrmlize = eL@(numpy.ones_like(matrixIn))@eR
    matrixOut = eL@matrixIn@eR
    matrixOut = matrixOut/nrmlize
    
    # matrixOut = torch.from_numpy(matrixOut)
    # matrixOut = matrixOut.to(device)
    
    return matrixOut