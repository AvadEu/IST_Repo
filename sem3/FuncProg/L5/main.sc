import annotation.tailrec

sealed trait Tree[+A]
case object Empty extends Tree[Nothing]
case class Node[A](value: A, left: Tree[A], right: Tree[A]) extends Tree[A]

def tree_sum(tree: Tree[Int]): Int = {
  @tailrec
  def sum_helper(workList: List[Tree[Int]], accumulator: Int): Int = {

    workList match {
      case Nil => accumulator

      case Empty :: tail =>
        sum_helper(tail, accumulator)

      case Node(v, l, r) :: tail =>
        sum_helper(l :: r :: tail, accumulator + v)
    }
  }
  sum_helper(List(tree), 0)
}


val tt = Node(1,
  Node(2,
    Node(4, Empty, Empty),
    Empty
  ),
  Node(3,
    Node(5,
      Empty,
      Node(6, Empty, Empty)
    ),
    Empty
  )
)
// 21
print(tree_sum(tt));

// 0
val test2 = Empty
print(tree_sum(test2));

// 100
val test3 = Node(100, Empty, Empty)
print(tree_sum(test3));

// 12
val test4 = Node(10, Node(5, Empty, Empty), Node(-3, Empty, Empty))
print(tree_sum(test4));