"""
Plot data from NIR sensor

Recordings taken with nir-recorder.py
Each recording is composed of: [Id, R,S,T,U,V,W]
Bands: 610, 680, 730, 760, 810 and 860nm


JCA
"""
import matplotlib.pyplot as plt
import numpy as np


CHANNELS = ['R','S','T','U','V','W']

def read_file(filepath):
    """Read file and return a list of arrays. Each row is a product with
    6 values corresponding to each NIR channel"""
    with open(filepath, 'r') as f:
        lines = f.readlines()

    lines = [l.strip().split(';')[1:] for l in lines]
    data = []
    for l in lines:
        data.append(np.array([float(i) for i in l]))
    return data

def distance_plot():
    """Plot Products at different distances from NIR sensor
    5 products at 3 distances (2cm, 4cm, 6cm)    
    """
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/distance-test.txt'

    def product_plot(ax, values, color, label):
        """Plot 3 observations of the same produc"""
        colors = ['red', 'yellow', 'blue']
        labels = ['2cm', '4cm', '6cm']
        for i in range(3):
            ax.bar(CHANNELS, values[i], color=colors[i], alpha=0.2, linewidth=0, width=1.0, zorder=-i)
            # Max
            if i==0: ax.plot(CHANNELS, values[i], '.-', c=color, linewidth=1, label=label)
    
    products = {
        0:	'Coca-Cola Lata',
        1:	'Botella Cristal',
        2:	'Vaso Nikkei',
        3:	'Yogurt Griego',
        4:	'Oreo'
    }

    lines = np.array(read_file(filepath))
    lines = (lines-np.mean(lines, axis=0)) / np.std(lines, axis=0)

    fig, ax = plt.subplots()

    i=0
    prod = [] # Three measures of the same product
    colors = ['aqua', 'yellow', 'black', 'lime', 'dodgerblue']
    prod_n = 0 # Id of the product
    # Scale factor 
    s = 20
    scale = np.array([1,5,s,s,s,s])
    prod_is = 0
    for l in lines:
        i += 1
        obs = l #+ abs(np.min(l))#* scale
        prod.append(obs)
        if i%3==0:
            product_plot(ax, prod, colors[prod_n], products[prod_n])
            i=0
            prod = []
            prod_n += 1
    
    plt.legend()
    plt.show()


def pca_reduction(data, ax=3):
    """Principal Component Analysis. return data reduced to ax dimensions"""
    x = (data-np.mean(data, axis=0)) / np.std(data, axis=0)
    z = np.dot(x.T, x) # Covariance matrix
    eigenvalues, eigenvectors = np.linalg.eig(z)

    variance_explained = []
    for i in eigenvalues:
        variance_explained.append((i/sum(eigenvalues))*100)
            
    print(f'Variance Explained: {variance_explained}')

    projection_matrix = (eigenvectors.T[:][:ax]).T

    return np.dot(x, projection_matrix)


def same_product():
    """Plot measures of the same product on different positions"""
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/oreo-positions.txt'
    x = np.array(read_file(filepath))
    # x = (data-np.mean(data, axis=0)) / np.std(data, axis=0)

    fig, ax = plt.subplots()

    for row in x:
        ax.plot(CHANNELS, row, '.--', c='black', linewidth=1)

    std = np.std(x, axis=0)
    ax.bar(CHANNELS, std, color=['crimson', 'orange', 'gold', 'chartreuse', 'springgreen', 'aquamarine'], linewidth=0, width=1.0)
    # plt.legend()
    plt.show()

def dataset_plot():
    """Plot all the data in the 6 bands"""
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/products.txt'
    data = np.array(read_file(filepath))

    x = pca_reduction(data)

    # Materials
    colors = ['orangered', 'darkorange', 'darkolivegreen', 'dodgerblue', 'darkblue', 'crimson']
    materials={
        0:'plastic',
        1:'paper',
        2:'other',
        3:'glass',
        4:'metal',
        5:'organic'
    }
    material_filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/products_material.txt'
    with open(material_filepath, 'r') as f:
        mats = f.readlines()
    cols = [colors[int(m.strip())] for m in mats]

    # Plot
    fig, ax = plt.subplots()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x[:,0],x[:,1],x[:,2], c=cols, s=15)
    
    # ax.scatter(x[:,0],x[:,1], c=cols, s=10)

    markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in colors]
    plt.legend(markers, materials.values(), numpoints=1)
    plt.show()


def lights():
    """Measument with ambient light vs dark. The first 5 lines are with light"""
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/lights.txt'
    x = np.array(read_file(filepath))

    products = {
        0:	'Coca-Cola Lata',
        1:	'Botella Cristal',
        2:	'Vaso Nikkei',
        3:	'Yogurt Griego',
        4:	'Oreo'
    }

    light_on = x[:5,:]
    light_off = x[5:,:]
    diff = abs(light_off-light_on)

    fig, ax = plt.subplots()
    colors = ['aqua', 'yellow', 'black', 'lime', 'dodgerblue']
    i=0
    # Scale factor for channel
    s = 20
    scale = np.array([1,5,s,s,s,s])
    for on,off in zip(light_on, light_off):
        on *= scale
        off *= scale
        ax.plot(CHANNELS, on, '.-', c='black')
        ax.plot(CHANNELS, off, '.--', c='black')
        ax.fill_between(CHANNELS, off, on, color=colors[i],
                 alpha=0.5)
        i+=1

    markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in colors]
    plt.legend(markers, products.values(), numpoints=1)

    plt.show()



def main():
    # distance_plot()
    # dataset_plot()
    # same_product()
    lights()


if __name__ == '__main__': main()