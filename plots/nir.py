"""
Plot data from NIR sensor

Recordings taken with nir-recorder.py
Each recording is composed of: [Id, R,S,T,U,V,W]
Bands: 610, 680, 730, 760, 810 and 860nm


JCA
"""
import os

import matplotlib.pyplot as plt
import numpy as np

from auxfunc import pca_reduction, convex_hull, read_file


CHANNELS = ['R','S','T','U','V','W']


def distance_plot():
    """Plot Products at different distances from NIR sensor
    5 products at 3 distances (2cm, 4cm, 6cm)    
    """
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/distance-test.txt'

    def product_plot(ax, values, color, label):
        """Plot 3 observations of the same produc"""
        colors = ['red', 'deepskyblue', 'darkblue']
        labels = ['2cm', '4cm', '6cm']
        for i in range(3):
            ax.bar(CHANNELS, values[i], color=colors[i], alpha=0.2, linewidth=0, width=1.0, zorder=i)
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
    # lines = (lines-np.mean(lines, axis=0)) / np.std(lines, axis=0)

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
        obs = l * scale #+ abs(np.min(l))#
        prod.append(obs)
        if i%3==0:
            product_plot(ax, prod, colors[prod_n], products[prod_n])
            i=0
            prod = []
            prod_n += 1
    
    plt.legend()
    plt.show()


def case_vs_dark():
    """Plot distance plots in dark room vs same products with case
    File structure:
    (For product)
    1 meassure with case
    2 meassure in dark room
    """
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/with_case/case_test-products.txt'

    def product_plot(ax, values, color, label):
        """Plot 2 observations of the same produc"""
        line_style=['-', '--']
        for i in range(2):
            ax.plot(CHANNELS, values[i], line_style[i], color=color)
        ax.fill_between(CHANNELS,  values[0],  values[1], color=color,
                 alpha=0.3, label=label)
    
    products = {
        0:	'Coca-Cola Lata',
        1:	'Botella Cristal',
        2:	'Vaso Nikkei',
        3:	'Yogurt Griego',
        4:	'Oreo'
    }

    lines = np.array(read_file(filepath))
    # lines = (lines-np.mean(lines, axis=0)) / np.std(lines, axis=0)
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
        obs = l * scale
        prod.append(obs)
        if i%2==0:
            product_plot(ax, prod, colors[prod_n], products[prod_n])
            i=0
            prod = []
            prod_n += 1
    
    plt.legend()
    plt.show()


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


def same_product_case():
    """Same product different positions and with case vs dark room"""
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/oreo-positions.txt'
    x_dark = np.array(read_file(filepath))

    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/with_case/oreo_positions_case.txt'
    x_case = np.array(read_file(filepath))

    fig, ax = plt.subplots()

    # Scale factor 
    s = 20
    scale = np.array([1,5,s,s,s,s])

    for row in x_dark: ax.plot(CHANNELS, row*scale, '.--', c='black', linewidth=1)
    for row in x_case: ax.plot(CHANNELS, row*scale, '.--', c='red', linewidth=1)
    plt.show()


def dataset_plot_one():
    """Plot all the data in the 6 bands. One measure by product on dark room"""
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


def dataset_plot(plot):
    """Dataset test plot with case and dark room. Each product is measure 5 times in different positions. 
        Each file contains 5 measures of the product. The filename starts with the ID of the product
        :param plot: (String) type of plot to make:
            - scatter
            - channel
            - submaterials
            - scatter-no-plastic
    """
    src_plot = plot
    # Materials
    colors = ['fuchsia', 'darkorange', 'darkolivegreen', 'dodgerblue', 'darkblue', 'crimson']

    materials={
        0:'plastic',
        1:'paper',
        2:'other',
        3:'glass',
        4:'metal',
        # 5:'organic'
    }
    material_filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/products_material.txt'
    with open(material_filepath, 'r') as f:
        mats = f.readlines()
    mats = [int(m) for m in mats]


    # SCATTER PLOT OF SUBMATERIALS
    title = None
    if plot == 'submaterials':
        title = 'Dataset Sub-materials - PCA'
        
        colors = ['fuchsia', 'darkorange', 'darkolivegreen', 'dodgerblue', 'darkblue', 'crimson', 'blue', 'red', 'green', 'cyan', 'black', 'slategray']

        materials = {
            0: 'plastic',
            1: 'other-plastic',
            2: 'PE',
            3: 'PS',
            4: 'PP',
            5: 'paper',
            6: 'other',
            7: 'glass',
            8: 'steel',
            9: 'copper',
            10: 'aluminum',
            11: 'organic'

        }
        material_filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/submaterials_id.txt'
        with open(material_filepath, 'r') as f:
            mats = f.readlines()
        mats = [int(m) for m in mats]

        plot = 'scatter'

    
    filepath = '/Users/juanca/Library/Mobile Documents/com~apple~CloudDocs/Projects/Sasvar/Dataset/Sensors/NIR/recordings/with_case/dataset-test'
    dataset_mats = [] # List of each observation material
    data = []
    for f in os.listdir(filepath):
        filename = os.path.join(filepath, f)
        m = mats[int(f.split('_')[0])]
        
        # SCATTER WITHOUT PLASTICS
        if plot == 'scatter-no-plastic' and m==0:
            continue

        dataset_mats += [m for i in range(5)]
        obs = read_file(filename)
        data += obs 
    data = np.array(data)
    cols = [colors[m] for m in dataset_mats]

    # SCATTER WITHOUT PLASTICS
    if plot == 'scatter-no-plastic': plot = 'scatter'



    # SCATTER PLOT
    if plot == 'scatter':
        title = 'Dataset Materials - PCA' if not title else title
        fig, ax = plt.subplots()

        # Plot each observation with a material-color correspondence
        x = pca_reduction(data)

        # Calculate Convex hull 
        if src_plot != 'submaterials':
            x_ = np.array([x[:,0],x[:,1]]).T
            obs_mat = get_obs_by_mat(dataset_mats, x_, no_mats=len(materials))

            for m, obs in obs_mat.items():
                try:
                    hull = convex_hull(obs.T)
                    ax.fill(hull[:,0], hull[:,1], color=colors[m], alpha=0.2)
                except AssertionError:
                    print('Not enough points')
        
        ax.scatter(x[:,0],x[:,1], c=cols, s=4)

        markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in colors]
        plt.legend(markers, materials.values(), numpoints=1)
        plt.title(title)
        plt.show()

    # CHANNEL PLOT
    if plot == 'channel':
        fig, ax = plt.subplots()
        data_norm = (data-np.mean(data, axis=0)) / np.std(data, axis=0)
        
        obs_mat = get_obs_by_mat(dataset_mats, data_norm, no_mats=len(materials))
        
        # Set material channels in a list
        for mat, obs in obs_mat.items():
            channels = [column for column in obs.T]
            violin_parts = ax.violinplot(channels)
            for pc in violin_parts['bodies']:
                pc.set_facecolor(colors[mat])
                pc.set_alpha(0.2)
                # pc.set_edgecolor(colors[mat])
            violin_parts['cmaxes'].set_color(colors[mat])
            violin_parts['cmaxes'].set_linewidth(1)

            violin_parts['cmins'].set_color(colors[mat])
            violin_parts['cmins'].set_linewidth(1)

            violin_parts['cbars'].set_color(colors[mat])
            violin_parts['cbars'].set_linewidth(1)

        
        markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in colors]
        plt.legend(markers, materials.values(), numpoints=1)
        plt.title('Materials Distribution by Channel')
        plt.show()


def get_obs_by_mat(dataset_mats, data_norm, no_mats=5):
    """Return observations by material {mat: obs}"""
        # append the index of the observation by material idx
    obs_idx_mat = {i:[] for i in range(no_mats)}
    for i, j in enumerate(dataset_mats): obs_idx_mat[j].append(i)
    
    # Get observations by material
    # Append observations to a dict to its corresponding material idx
    obs_mat = {}
    for i in range(no_mats):
        obs_mat[i] = np.take(data_norm, obs_idx_mat[i], axis=0)
    return obs_mat

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
    ## Plots with dark room
    # distance_plot()
    # dataset_plot_one()
    # same_product()
    # lights()

    ## Plots with case
    # case_vs_dark()
    # same_product_case()
    dataset_plot('scatter')
    # dataset_plot('submaterials')
    # dataset_plot('scatter-no-plastic')
    # dataset_plot('channel')
    

if __name__ == '__main__': main()