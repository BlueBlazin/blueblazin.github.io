---
layout: post
title:  "Introduction to Recursion; or Wishful Thinking"
date:   2017-11-07
categories: Computer Science
---



## Introduction

This post introduces recursion using three examples -- reversing a linked list, the towers of Hanoi problem, and deletion in a binary search tree. This article assumes no prerequisites other than familiarity with a programming language (I'll use python but you can easily follow along even if you aren't familiar with it).



## Wishful Thinking

Recursion is a top-down approach to solving problems where you solve easier sub-problems and use their solutions to solve larger problems ultimately solving the problem you set out to solve. It's essential that these sub-problems are structurally identical to the larger problem, but easier to compute in general. 

So the essense of a recursive function is to call itself on instances of easier sub-problems. These function calls in turn can call the same function again, and so on until some base case is reached whereupon the solution to these simplest sub-problems becomes obvious and can be computed directly. 

These chains of recursive calls makes it hard to wrap your head around recursion. Understanding it from a bottom up perspective can get overwhelming very quickly. 

So it's easier to look at it from a top down point of view. That's where wishful thinking comes into picture. So much so, that I feel recursion isn't just best understood using wishful thinking, but rather __it is__ wishful thinking!

But that's a lot of words, let's dive straight into it now, with our first problem being that of reversing a singly linked list.



## Reversing a Linked List

A linked list is a data structure containing nodes linked by arrows. In a typical singly linked list, each node contains some data, and an arrow to the next node. As you can guess, a doubly linked list node contains arrows to both the next, and previous nodes.

![linked list](https://upload.wikimedia.org/wikipedia/commons/6/6d/Singly-linked-list.svg "Singly Linked List"){: .center-image }

Defining a (singly) linked list in python is very easy. We just define a class:

```python
class Node:
  def __init__(self, value):
    self.value = value
    self.next = None
```

Okay, that's straightforward. To make a new linked list you just create multiple nodes and then chain them appropriately:

```python
head = Node(12)
head.next = Node(99)
head.next.next = Node(37)
```

It doesn't have to be this cumbersome, we can actually write a function that takes a python list and converts it to a linked list:

```python
def make_list(l):
  head = Node(l[0])
  current = head
  for value in l[1:]:
    current.next = Node(value)
    current = current.next
  return head
```

The last thing is to be able to print out the list:

```python
def print_list(node):
  l = []
  while node:
    l.append(node.value)
    node = node.next
  print(l)
```

I'm being this explicit only because this is the first example. For the others, I won't write out the code for all helper functions. Also, note that I'm not doing any tests, checks, or assertions. These are extraneous to the topic being discussed, and I expect you are already aware of how to use them. Anyways, with that out of the way let's move on to the real task at hand: given a head node, we want to reverse the list.

This means that our `reverse_list` function should take the first node, and return the last node, with all links between nodes reversed. 

```python
def reverse_list(first):
  return last
```

This is it! Our first encounter with wishful thinking. We wish for two things, 1. to get the last node of the list, 2. to reverse all the links.

We use wishful thinking to assume that the list is reversed from the second node onward, and that we are returned the last node.

```python
def reverse_list(first):
  last = reverse_list(first.next)
  return last
```

Great! Just like that, we now have our old first node, a reversed list from the second node to the last node, and a pointer to the last node. The only thing we need to do now is to have `second.next` point to `first`, and `first.next` equal `None` (a.k.a point to nothing). 

```python
def reverse_list(first):
  last = reverse_list(first.next)
  first.next.next = first  # second was first.next in the unreversed list
  first.next = None
  return last
```

At this point we're almost done. The only thing that remains is to deal with the so called 'base case' of when first doesn't have a `next`. In that case we just return first. In other words, if the list was just a single node, then its reverse is the same as itself.

```python
def reverse_list(first):
  if first.next is None: return first
  last = reverse_list(first.next)
  first.next.next = first
  first.next = None
  return last
```

We can test this, for example:

```python
l = make_list([1, 2, 3, 4, 5])
print_list(l)
rl = reverse_list(l)
print_list(rl)
```

The output will be: 

```
[1, 2, 3, 4, 5]
[5, 4, 3, 2, 1]
```

If you're used to a bottom-up way of thinking about things, this could be a little hard to accept. But with practice you can develop an ability to use wishful thinking, and recursion will reduce to simply a matter of thinking boldly.



## Towers of Hanoi

Our next problem is one of the most famous examples used when teaching recursion. You have three poles, $A$, $B$, and $C$, and disks of various sizes placed on the poles.

![poles and disks](https://upload.wikimedia.org/wikipedia/commons/0/07/Tower_of_Hanoi.jpeg "Towers of Hanoi"){: .center-image }

We want to move the stack of disks from pole $A$, to pole $C$. You may use any of the three poles during the task, but in the end all disks from pole $A$ need to be on pole $C$. During the intermediate steps, you can only remove the topmost disk from a stack, and at any point disks on the stacks must be in descending order of size from bottom to top. The problem asks us to return a list of all moves we must perform in order to move the stack on $A$ to $C$.

Let's label the disks from $1$ to $n$, $1$ being the topmost disk on the stack. With wishful thinking, the solution to this seemingly complicated problem is as simple as just describing the problem in English.

```python
def hanoi(n, source, dest, spare):
```

The function hanoi has four parameters -- `n` is the number of disks, `source` is the starting pole, `dest` is the destination pole, and `spare` is the extra spare pole. If you think about it for a minute or two, a general strategy will come to you. Move the first $n-1$ disks from pole $A$ to pole $B$ obeying the rules. Move disk $n$ from pole $A$ to pole $C$. Move the $n-1$ disks from $B$ to $C$, and we're done. No rules were violated and we moved all disks from $A$ to $C$. Believe it or not, the solution in code is exactly that!

```python
def hanoi(n, source, dest, spare):
  hanoi(n-1, source, spare, dest)
  print("Move disk {} from pole {} to pole {}".format(n, source, dest))
  hanoi(n-1, spare, dest, source)
```

That's it! The first line states that we use our procedure to move the top $n-1$ disks to `spare` as destination, using `dest` as the spare pole. Then we move the largest disk from source to destination. Finally we move the $n-1$ disks from the spare pole to the destination pole. The only thing remaining is a base case. That's when n is zero, we don't do anything.

```python
def hanoi(n, source, dest, spare):
  if n < 1: return
  hanoi(n-1, source, spare, dest)
  print("Move disk {} from pole {} to pole {}".format(n, source, dest))
  hanoi(n-1, spare, dest, source)
```

If we call this function with arguments `n=3`, `source="A"`, `dest="C"`, and `spare="B"`, we get this output:

```
Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C
```



## Deletion In Binary Search Trees

![binary search tree](https://upload.wikimedia.org/wikipedia/commons/d/da/Binary_search_tree.svg "Binary Search Tree"){: .center-image }


A tree is by definition a recursive data structure. It's a linked data structure like linked lists, except instead of having a single next 'link', a tree node can have multiple 'children'. A tree usually has a root node, which may have links to several child nodes. These can themselves be thought of as root nodes to their own children, and are thus called 'sub-trees'. Thus, trees are recursive and many tree algorithms can be implemented elegantly using recursion. 

A binary tree is a special type of tree where each node has at most two children -- left, and right. A binary search tree is a special type of binary tree where every node in the left subtree of a node has value less than its value, and every node in the right subtree has a greater value.

Binary Search Trees (BSTs) can be used to implement binary search, an efficient search algorithm that takes $O(log\:n)$ time to check if an element is in the tree and return it.

The algorithm for binary search is very simple:

```python
def search(root, value):
  if root is None: return None
  if value == root.value: return value
  return search(root.left) if value < root.value else search(root.right)
```

If the value is equal to the root node's value, return it. If it isn't, return the result of calling search on the left subtree if the value is less than the roots value, else the result of search on the right subtree.

The other base case is when the root node is `None`, in which case the value wasn't found and we return `None`.

Back to deletion, the algorithm can be a little tricky. We must maintain the BST property after the deleting the element (if it exists). There are three different cases depending on the number of children the node to be deleted has.

### Algorithm for Deletion

In case you skipped the wall of text above, here's the deletion algorithm. The three cases that can arise when deleting an element are as follows:

- The element has no children
- The element has one child
- The element has two children

The first case is almost trivial, we just set the node to `None`. If the node has one child, we set the node to point to that child instead. Doing that, along with some clever recursive code spares us from storing parent pointers or having unnecessary ugly code.

The Final case is the trickiest, where a node has both its children. In that case we'll first find the node with the largest value less than our node's value. That simply means we find the rightmost node from the left subtree. Once we have it, we'll save its value, set it to `None`, and change our node's value to this saved value.

Why does that work? Well, the node we found was from the left subtree so every element in the right subtree still has a greater value than it. Also, it had the biggest value from the left subtree, so all the other remaining elements in the left subtree will have a value less than it. So, the BST property is retained.

Finally, the code:

```python
def delete(root, key):
  if   key < root.value: root.left = delete(root.left, key)
  elif key > root.value: root.right = delete(root.right, key)
  else: # key == root.value
```

What's happening here? Given a key (the element), we first have to find the node with that value. This is just binary search. Since we want to deal with the possibility that no node with the given key's value exists, let's handle it first.

```python
def delete(root, key):
  if root is None: return None
  if   key < root.value: root.left = delete(root.left, key)
  elif key > root.value: root.right = delete(root.right, key)
  else:
    # TODO: implement case where node with value equal to key is found
  return root
```

While this bit looks easy, there's actually something subtle and interesting going on here. We aren't just calling `delete(root.left, key)` for example, we're setting `root.left` equal to it! I mentioned above that we'll use some clever recursive code to avoid having parent pointers and ugly addon code. That clever recursive bit isn't just helping keep the code elegant, it's actually directly applying our old friend: 

**Wishful Thinking!**

What is it that we wish to do if we knew that the key we want to delete is in the left subtree of our root node? Why, we want to point `root.left` to the subtree where the node with value equal to this key is deleted and everything has been taken care of of course!

And that's exactly what we're doing. We're simply setting `root.left`, or `root.right` to this subtree which has had the correct node deleted, and its BST property restored. That's some extreme wishful thinking but it will all work out in the end.

Now, let's move on to the main task of actually deleting the node once it's found using our three cases. We're gonna handle case 1, and one half of case 2 together, in a single line of code!

```python
def delete(root, key):
  if root is None: return None
  if   key < root.value: root.left = delete(root.left, key)
  elif key > root.value: root.right = delete(root.right, key)
  else:
    if root.left if None: return root.right
  return root
```

Since our implementation of case three depends on finding the rightmost child from the left subtree, the left subtree can't be `None`. So if it is, we simply return `root.right`. If `root` had no children, this would just return `None` which would propagate up through the recursive call and set the appropriate child of our root's parent to `None`. No need for parent pointers or checks for which child of the parent the deleted node belonged to. This also handles the case when the node to be deleted has a single right child.

Now let's focus on case 3, since case 2 with a single left child is handled automagically by just considering case 3.

```python
def delete(root, key):
  if root is None: return None
  if   key < root.value: root.left = delete(root.left, key)
  elif key > root.value: root.right = delete(root.right, key)
  else:
    if root.left is None: return root.right
    tmp = root
    root = get_max(root.left)
    root.left = del_max(tmp.left)
    root.right = tmp.right
  return root
```

First, create a temporary variable that points to the same node as `root`. This is needed because `root` will itself soon point to the rightmost child of the left subtree. We set root to the highest valued node (rightmost child) in the left subtree using the `get_max` function.

Once `root` is pointing to it, we'll set its parent to point to `None` instead. In other words, we'll delete this rightmost node using `del_max`. The node itself isn't deleted per se, it's just not pointed to by its parent anymore. The `root` node is still pointing to it, so it's safe.

Finally, we point our new `root`'s right child to the old `root`'s right child, which was stored safely in `tmp`. Finally we return `root`. This will propagate up through the chain of recursive calls, correctly setting left and right subtrees of parents to new subtrees with the correct node deleted and the BST property intact. Here's the full code:

```python
def delete(root, key):
  if root is None: return None
  if   key < root.value: root.left = delete(root.left, key)
  elif key > root.value: root.right = delete(root.right, key)
  else:
    if root.left if None: return root.right
    tmp = root
    root = get_max(root.left)
    root.left = del_max(tmp.left)
    root.right = tmp.right
  return root

def get_max(root):
  if root.right is None: return root
  return get_max(root.right)

def del_max(root):
  if root.right is None: return root.left
  root.right = del_max(root.right)
  return root
```

By now, you have enough experience with wishful thinking to analyze the two functions `get_max`, and `del_max` yourself. The `del_max` function in particular is a microcosm of the larger `delete` algorithm. Go ahead and apply wishful thinking to understand how it works.

## Conclusion

Hopefully seeing these three examples of recursion in action will help you understand how you can use it to solve some challenging problems. We can branch off in a couple directions now. We can look at a problem solving strategy that employs recursion to break down problems into (not one but) multiple simpler subproblems only to build the final solution back up from these 'sub-solutions'. This is the so called 'Divide and Conquer' strategy. We could also look at a (optionally) recursive strategy that solves problems where subproblems overlap. This is 'Dynamic Programming', where we keep a record of solutions to subproblems we've already solved, so we can just look them up whenever possible. Last but not the least, we could look at mutual recursion. Here two or more recursive functions call each other. Some complex recursive problems can be broken down into multiple mutually recursive functions that make the code more elegant and easy to read. But all of these are topics for another day. 

For today, I just want you to take away that if you choose to employ wishful thinking to solve problems with recursion - think boldly, and delay implementing the base case until the end.