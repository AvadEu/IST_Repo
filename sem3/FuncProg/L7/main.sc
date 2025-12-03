def ldzialanie[A](l1: LazyList[A], l2: LazyList[A], op: (A, A) => A): LazyList[A] = {
  (l1, l2) match {
    case (LazyList(), LazyList()) => LazyList()
    case (LazyList(), rest) => rest
    case (rest, LazyList()) => rest
    case (h1 #:: t1, h2 #:: t2) =>
      op(h1, h2) #:: ldzialanie(t1, t2, op)
    case _ => LazyList()
  }
}

val div = (x: Int, y: Int) => {
  if (y == 0) throw new ArithmeticException("Nie wolno dzielić przez 0!")
  else x / y
}

val l1 = LazyList(1, 2, 3)
val l2 = LazyList(2, 3, 4, 5)
println(ldzialanie(l1, l2, (x: Int, y: Int) => x + y).toList)
println(ldzialanie(l1, l2, (x: Int, y: Int) => x * y).toList)
println(ldzialanie(l1, l2, (x: Int, y: Int) => x - y).toList)



val l3 = LazyList(10, 20, 30, 40)
val l4 = LazyList(2, 5, 0, 4)
println(ldzialanie(l3, l4, div).toList)