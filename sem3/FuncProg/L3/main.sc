import scala.annotation.tailrec

@tailrec
def reverse(list: List[Int], acc: List[Int] = Nil): List[Int] = {
    list match {
        case Nil => acc
        case head :: tail => reverse(tail, head :: acc)
    }
}

def mult(listA: List[Int], listB: List[Int]): List[Int] = {
    @tailrec
    def mult_in(acc: List[Int], lstA: List[Int], lstB: List[Int]): List[Int] = {
    (lstA, lstB) match {
        case (Nil, Nil) => reverse(acc)
        
        case (headA :: tailA, headB :: tailB) =>
        mult_in((headA * headB) :: acc, tailA, tailB)

        case (Nil, headB :: tailB) =>
        mult_in((1 * headB) :: acc, Nil, tailB)

        case (headA :: tailA, Nil) =>
        mult_in((1 * headA) :: acc, tailA, Nil)
        }
    }
    mult_in(Nil, listA, listB)
}

mult(List(1, 2, 3), List(4, 5))
mult(List(1, 2, 3, 1, 2 ,3), List(0, 0, 0))
mult(List(10, 20,30), List())
mult(List(), List(10, 20,30))