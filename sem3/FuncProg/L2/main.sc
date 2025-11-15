import scala.annotation.tailrec

def len[A](arr: List[A]): Int = {
    @tailrec
    def lenIn(x: List[A], acc: Int): Int = x match {
    case Nil => acc
    case _ :: tail => lenIn(tail, acc + 1)
}
    lenIn(arr, 0)
}

len(List(1, 2, 3, 4, 5))
len(List())
len(List(1))
len(List.range(1, 10_000_000))
