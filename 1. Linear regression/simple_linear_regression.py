import numpy
import math
import os
import metrics

max_gen = 5000


def get_direction(v):
    norm = numpy.linalg.norm(v)
    return numpy.asarray([x / norm for x in v])


def compute(X, Y, eps, learning_rate, w, output_file, full_output = False):
    #   Print initialization values
    output_file.write('Mode: simple\n')
    output_file.write('Eps: %f\n' % eps)
    output_file.write('Learning rate: %f\n' % learning_rate)
    output_file.write('Initial w: %s\n' % w)
    output_file.write('Max generation: %d\n' % max_gen)
    output_file.write('\n')

    output_file.flush()
    os.fsync(output_file.fileno())    

    #   Calculate general values
    total = Y.size
    y_mean = Y.mean()
    y_var = Y.var()
    
    gradient = [0] * X.shape[1]
    loss = 0
    cur_gen = 0

    while cur_gen < max_gen:
        gradient = [0] * X.shape[1]
        cur_gen += 1

        if full_output:
            (loss, r_2, rmse) = metrics.calculate(X, Y, w)
            gradient = metrics.calculate_gradient(X, Y, w)
            
            output_file.write('Generation: %d\n' % cur_gen)
            output_file.write('Loss: %f\n' % loss)
            output_file.write('R2: %f\n' % r_2)
            output_file.write('RMSE: %f\n' % rmse)
            output_file.write('Gradient: %s\n' % gradient)
            output_file.write('W: %s\n' % w)
            output_file.write('\n')

            #   Flush changes to file
            if cur_gen % 100 == 0:
                output_file.flush()
                os.fsync(output_file.fileno())

            print("Gen: %5d | Loss: %5.2f | R2: %5.3f | RMSE: %.3f" % (cur_gen, loss, r_2, rmse))           
        else:
            gradient = metrics.calculate_gradient(X, Y, w)    
        
        gradient_dir = get_direction(gradient)
        w = w - gradient_dir * learning_rate * (1 / math.log(cur_gen + 1))
    return w