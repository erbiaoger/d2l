import numpy as np

def model_gen(vs, vp, rho, z, n):
    model = {}
    model['vsv'] = []
    model['vpv'] = []
    model['rhov'] = []
    model['h'] = []

    for i in range(len(n)):
        model['vsv'] += [vs[i]] * n[i]
        model['vpv'] += [vp[i]] * n[i]
        model['rhov'] += [rho[i]] * n[i]
        model['h'] += [z[i]] * n[i]

    model['Nn'] = len(model['h'])
    model['hzcum'] = np.cumsum(model['h'])
    model['vsv'] = np.array(model['vsv'])
    model['vpv'] = np.array(model['vpv'])
    model['rhov'] = np.array(model['rhov'])
    model['h'] = np.array(model['h'])
    
    return model


if __name__ == '__main__':
    # Example usage:
    vs = [1.5, 2.0, 3.0]
    vp = [2.5, 3.5, 4.5]
    rho = [1.8, 2.0, 2.2]
    z = [10, 20, 30]
    n = [2, 3, 1]

    result_model = model_gen(vs, vp, rho, z, n)
    print(result_model)
