---
layout: post
title:  "Eigenvalue Decomposition"
date:   2016-08-18 
categories: Math
---


## Table of Contents

1. [Introduction](#introduction)
2. [Eigenvalues & Eigenvectors](#eigenvalues--eigenvectors)
3. [Finding Eigenvalues & Eigenvectors](#finding-eigenvalues--eigenvectors)
4. [The Eigendecomposition](#the-eigendecomposition)
5. [Applications - Powers of A](#applications---powers-of-a)
6. [References](#references)



## Introduction

Let's talk about the Eigenvalue Decomposition! You're most certainly familiar with the concept of a function. In the world of mathematics, there exist these special type of functions called *Linear Transformations*. There are two properties that all linear maps (or transforms) $T$ must obey:

$$T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$$,


$$T(c \mathbf{u}) = c T(\mathbf{u}) \:$$  for any scalar $c$.


But Linear Maps have a dirty little secret! Every linear map (provided it is over [finite dimensional vector spaces](https://en.wikipedia.org/wiki/Dimension_(vector_space))) can be represented as a Matrix, and every Matrix represents a linear map!

Matrices can represent complicated functions, but much like numbers, matrices can be factored (or decomposed). Thus a complicated matrix can be written instead as a product of simple and beatiful matrices. The decomposition we'll study today is the eigen decomposition. There are many others as well, for example - the famous Singular Value Decomposition (SVD) - which will be the topic of another post. 

The eigendecomposition will be possible with only square matrices with no repeated eigenvalues. So before we begin, let's quickly review eigenvalues and eigenvectors. 



## Eigenvalues & Eigenvectors

Let $A$ be an $(N \times N)$ matrix. As I mentioned in the introduction, matrices represent linear transformations of vectors. That means, applying a matrix to a vector transforms (scales and rotates) it. Are there any vectors that do not change direction under the transformation? 

As it turns out, for any $A$, if we choose our Field (the set our scalars belong to) to be $\mathbb{C}$, the complex numbers, then we are guaranteed at least one such vector.

**Theorem:** Every matrix $A$ over the complex field has an eigenvector.

**Proof:**
Choose any nonzero vector $\mathbf{v} \in \mathbf{V}$ of dimension $n$. Then the collection of vectors:

$\mathbf{v}, A \mathbf{v}, A^2 \mathbf{v}, ..., A^n \mathbf{v}$ is linearly dependent.

Thus there exists some linear combination of these vectors:

$$a_0\mathbf{v} + a_1 A \mathbf{v} + ... + a_n A^n \mathbf{v} = 0$$ with not all $a's$ zero. 

$$ = \sum_{i=0}^n a_i A^i \mathbf{v} = 0$$,

$$ = P(A)\mathbf{v} = 0$$, 

where $p(t)$ is the polynomial $\sum_{i=0}^n a_i t^i$.

From the Fundamental Theorem of Algebra, every polynomial over $\mathbf{C}$ can be written as a product:

$$p(t) = c \prod(t - \lambda_i), \:\: c \neq 0$$.

$$\therefore p(A)\mathbf{v} = c \prod(A - \lambda_i I)\mathbf{v} = 0$$.

But remember $\mathbf{v}$ was non zero? Thus $\prod(A - \lambda_i I)$ maps the nonzero vector $\mathbf{v}$ to the zero vector $0$.
The only way for a matrix to have a non trivial null space is if it's non-invertible (invertible functions are one-to-one mappings and zero is always in the null space of any linear transform so invertible functions cannot have any one vectors mapping to zero). The product of invertible matrices is itself invertible, therefore $\prod(A - \lambda_i I)$ must contain at least one non-invertible matrix $A - \lambda_i I$. 

For such a matrix,


$$(A - \lambda_i)\mathbf{v} = 0$$ or


$$A \mathbf{v} = \lambda_i \mathbf{v}$$. 

This completes the proof that every matrix has at least one eigen vector over the complex field, and also provides us a way to compute it. $$\tag*{$\blacksquare$}$$


## Finding Eigenvalues & Eigenvectors

Okay, so this part will be very brief (apologies for the long proof in the last part). The determinant of non-invertible matrices is zero. This gives us a way of finding eigenvalues and eigenvectors. 

$$det(A - \lambda) = 0$$.

This gives us a polynomial equation to solve. Solving for the roots of this equation give us the eigenvalues. These can be unique or repeated, real or complex. 

For each eigenvalue, putting it into $det(A - \lambda)\mathbf{v} = 0$ and solving gives us the eigenvectors. This whole process is best understood by looking at examples, and most introductory linear algebra textbooks have many solved examples. Of course you can find a myriad examples on the internet as well. 


## The Eigendecomposition

I said at the beginning, some ugly matrices can be factored into a product of beautiful matrices. Eigendecomposition works only for square matrices, unlike the Singular Value Decomposition which works for rectangular matrices as well. Further more, the matrix must have a full set of linearly independent eigenvectors. 

If these conditions are met for a matrix $A$, we can arrange $A's$ eigenvectors in it's own matrix:

$$S = \begin{bmatrix}\mathbf{x_1} & \mathbf{x_2} & \ldots \mathbf{x_n}\end{bmatrix}$$.

And upon multiplying this matrix by $A$, we get:

$$AS = \begin{bmatrix}A\mathbf{x_1} & A\mathbf{x_2} & \ldots A\mathbf{x_n}\end{bmatrix}$$,

$$\therefore AS = \begin{bmatrix} \lambda_1 \mathbf{x_1} & \ldots & \lambda_n \mathbf{x_n}\end{bmatrix}$$.

We can factor this into the product of $S$ and a diagonal matrix (zeros everywhere except on the diagonal) $\Lambda$ of eigenvalues.

$$AS = S \begin{bmatrix} \lambda_1 & 0 & \ldots & 0 \\ 0 & \lambda_2 & \ldots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \ldots & \lambda_n \end{bmatrix} = S\Lambda$$.

Since $S$ is a square matrix with linearly independent columns, it is invertible. Thus we arrive at our final equation:

$$A = S \Lambda S^{-1}$$. 

This is the decomposition of $A$ into a matrix of eigenvalues, a diagonal matrix, and the inverse of the eigenvalue matrix. Because all three of these are special matrices, we can use this decomposition to do some very interesting things efficiently. 


## Applications - Powers of A

Diagonal matrices are great! Squaring a diagonal matrix is just squaring it's entries (try it out for 3x3). Next, consider:

$$A\mathbf{x} = \lambda \mathbf{x}$$. 

Multiplying by $A$ on the left, and using the fact that $\mathbf{x}$ is an eigenvector of $A$, we get:

$$A^2 \mathbf{x} = \lambda^2 \mathbf{x}$$. 

Thus we see that $A^2$ has the same eigenvectors as $A$, and the eigenvalues are squared. Since $A^2$ has the same eigenvectors as $A$, we can use the eigendecomposition of $A$ to write $A^2$ as:

$$A^2 = S\Lambda S^{-1} S\Lambda S^{-1} = S \Lambda^2 S^{-1}$$. 

We can repeat this process to find $A^k = S \Lambda^k S^{-1}$. As I said before, computing the powers of diagonal matrices is very easy, and if we know the eigenvectors of $A$, computing any power of $A$ hence becomes easy as well. 


## References

1. Axler, Sheldon. Linear Algebra Done Right. New York: Springer, 2000. Print.
2. Strang, Gilbert. Introduction to Linear Algebra. Wellesley, MA: Wellesley-Cambridge, 2009. Print.
3. Lax, Peter D., and Peter D. Lax. Linear Algebra and Its Applications. Hoboken, NJ: Wiley-Interscience, 2007. Print.
4. Gilbert Strang. 18.06SC Linear Algebra. Fall 2011. Massachusetts Institute of Technology: MIT OpenCourseWare, http://ocw.mit.edu. License: Creative Commons BY-NC-SA.
5. https://en.wikipedia.org/wiki/Linear_map