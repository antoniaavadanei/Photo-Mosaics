from parameters import *
import numpy as np
import pdb
import timeit

#returneaza un array cu indicii sortati dupa distantele culorilor medii 
def sorted_indexes(avg_colors, cul_medie_window):
    distances=np.zeros(len(avg_colors))
    for k in range(len(avg_colors)):
        distances[k] = np.sqrt(np.sum((np.float64(avg_colors[k])-np.float64(cul_medie_window))**2))
    return distances.argsort()

def add_pieces_grid(params: Parameters):
    start_time = timeit.default_timer()
    img_mosaic = np.zeros(params.image_resized.shape, np.uint8)
    N, H, W,C = params.small_images.shape
    h, w,c = params.image_resized.shape

    num_pieces = params.num_pieces_vertical * params.num_pieces_horizontal
    
    
    if params.criterion == 'aleator':
        for i in range(params.num_pieces_vertical):
            for j in range(params.num_pieces_horizontal):
                index = np.random.randint(low=0, high=N, size=1)
                img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W, :] = params.small_images[index]
                print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))

    elif params.criterion == 'distantaCuloareMedie':
        #calculam mediile culorilor pieselor din colectie
        dimension=(N,3)
        avg_colors=np.zeros(dimension)

        for i in range(N):
            avg_colors[i] = np.mean(params.small_images[i], axis=(0, 1))
            
        #cazul in care vrem vecini diferiti
        if params.different_neigh==True:
            #cream o matrice numita 'neigh', unde neigh[i,j] retine indicele piesei de mozaic pozitionata pe [i,j]
            neigh_size=(params.num_pieces_vertical,params.num_pieces_horizontal)
            neigh=np.zeros(neigh_size)
            for i in range(params.num_pieces_vertical):
                for j in range(params.num_pieces_horizontal):
                    img_window = params.image_resized[i*H:(i+1)*H,j*W:(j+1)*W,:].copy()

                    cul_medie_window=np.mean(img_window, axis=(0, 1))
                    
                    if i==0 and j==0:
                        idx = sorted_indexes(avg_colors,cul_medie_window)[0]
         
                    elif i==0 and j>0: # verificam ca piesa din stanga sa fie diferita de ce urmeaza sa pun pe pozitia curenta
                        if neigh[i,j-1]==sorted_indexes(avg_colors,cul_medie_window)[0]:
                            #alegem urmatorul minim
                            idx=sorted_indexes(avg_colors,cul_medie_window)[1]
                        else:
                            idx = sorted_indexes(avg_colors,cul_medie_window)[0]
                    elif i>0 and j==0: # verificam ca piesa de sus sa fie diferita de ce urmeaza sa pun pe pozitia curenta
                        if neigh[i-1,j]==sorted_indexes(avg_colors,cul_medie_window)[0]:   
                            #alegem urmatorul minim
                            idx=sorted_indexes(avg_colors,cul_medie_window)[1]
                            #idx=np.argmin(new_distances)
                        else:
                            idx = sorted_indexes(avg_colors,cul_medie_window)[0]
                    #cazul cand i>0 si j>0    
                    else:
                        if neigh[i-1,j]==sorted_indexes(avg_colors,cul_medie_window)[0]:
                            idx=sorted_indexes(avg_colors,cul_medie_window)[1]
                            if neigh[i,j-1]==sorted_indexes(avg_colors,cul_medie_window)[1]:
                                idx=sorted_indexes(avg_colors,cul_medie_window)[2]
                        elif neigh[i,j-1]==sorted_indexes(avg_colors,cul_medie_window)[0]:
                            idx=sorted_indexes(avg_colors,cul_medie_window)[1]
                            if neigh[i-1,j]==sorted_indexes(avg_colors,cul_medie_window)[1]:
                                idx=sorted_indexes(avg_colors,cul_medie_window)[2]        
                        else:
                            idx = sorted_indexes(avg_colors,cul_medie_window)[0]
                        
                    img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W,:] = params.small_images[idx]
                    neigh[i,j]=idx
                    
                    print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))
            
        else:

            for i in range(params.num_pieces_vertical):
                for j in range(params.num_pieces_horizontal):
                    img_window = params.image_resized[i*H:(i+1)*H,j*W:(j+1)*W].copy()

                    cul_medie_window=np.mean(img_window, axis=(0, 1))
                    
                    distances = np.zeros(N)
                        
                    idx = sorted_indexes(avg_colors,cul_medie_window)[0]


                    img_mosaic[i * H: (i + 1) * H, j * W: (j + 1) * W] = params.small_images[idx]
                    print('Building mosaic %.2f%%' % (100 * (i * params.num_pieces_horizontal + j + 1) / num_pieces))


    else:
        print('Error! unknown option %s' % params.criterion)
        exit(-1)

    end_time = timeit.default_timer()
    print('Running time: %f s.' % (end_time - start_time))

    return img_mosaic


def add_pieces_random(params: Parameters):
          
    
    h, w, c = params.image_resized.shape
    nr_pieces,h_piece, w_piece,c=params.small_images.shape
    #calculam mediile culorilor pieselor din colectie
    dimension=(nr_pieces,3)
    avg_colors=np.zeros(dimension)

    for i in range(nr_pieces):
        avg_colors[i] = np.mean(params.small_images[i], axis=(0, 1))
    
    #vrem sa adaugam o bordura de dimensiune h_piesa mozaic in partea de jos a imaginii redimensionate, si de dimensiune W_piesa mozaic in partea dreapta
    big_size=h+h_piece,w+w_piece,3
    

    big_image=np.zeros(big_size,dtype=np.uint8)
    cv.rectangle(big_image,(0,0),(h+h_piece,w+w_piece),(0,0,0)) # construim bordura neagra
    big_image[0:h,0:w,:]=params.image_resized 
    
    #cream o matrice de dimensiunea big_image in care stocam indicii pixelilor daca pixelul face parte din imagine, sau -1 daca pixelul e de pe bordura
    pixels_size=h+h_piece,w+w_piece
    pixels=np.zeros(pixels_size) 
    for i in range(pixels_size[0]):
        for j in range(pixels_size[1]):
            if i>=pixels_size[0]-h_piece or j>=pixels_size[1]-w_piece:
                pixels[i][j]=-1
            else:
                pixels[i][j]=i*w+j
                
        
    while True:
        #unused pixels contine pixeli care nu sunt acoperiti deja de o piesa de mozaic
        unused_pixels=pixels[pixels>-1]
        if len(unused_pixels)==0:
            break
        #alegem random un pixel care nu e acoperit de o piesa de mozaic
        index=int(np.random.randint(low=0,high=len(unused_pixels),size=1))
        
        #identificam linia si coloana pe care se afla indexul ales
        
        row=int(unused_pixels[index]/(w))
        col=int(unused_pixels[index]%(w))
        
        #extragem subimaginea de dimensiune h_piece, w_piece care incepe pe linia si coloana identificate
        img_window = big_image[row:row+h_piece,col:col+w_piece,:].copy()
        #calculam culoarea medie
        cul_medie_window=np.mean(img_window, axis=(0, 1))

        # distanta l2
        distances = np.zeros(nr_pieces)
        for k in range(nr_pieces):
            distances[k] = np.sqrt(np.sum((np.float64(avg_colors[k])-np.float64(cul_medie_window))**2))

        idx = np.argmin(distances)

        #inlocuim subimaginea identificata cu sablonul de distanta minima
        big_image[row:row+h_piece,col:col+w_piece,:] = params.small_images[idx]
        #populam cu -1 portiunea unde am asezat in imagine sablonul
        for i in range(row,row+h_piece):
            for j in range(col,col+w_piece):
                pixels[i][j]=-1
    big_image=big_image[0:h,0:w,:]
    return big_image


def add_pieces_hexagon(params: Parameters):
    return None
