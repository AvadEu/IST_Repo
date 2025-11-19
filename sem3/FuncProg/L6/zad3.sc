sealed trait Instr
case class Push(x: Int) extends Instr
case object Pop extends Instr
case object Inc extends Instr

type Stack = List[Int]

def eval(instructions: List[Instr]): Stack = {
  instructions.foldLeft(List[Int]()) { (stack, instr) =>
    (instr, stack) match {
      case (Push(x), s) => x :: s
      case (Pop, _ :: tail) => tail
      case (Pop, Nil) => Nil
      case (Inc, head :: tail) => (head + 1) :: tail
      case (Inc, Nil) => Nil
    }
  }
}

val t1 = eval(List(Push(3), Push(5), Inc))
println(s"Test 1: $t1") // List(6, 3)

val t2 = eval(List(Push(10), Push(20), Pop))
println(s"Test 2: $t2") // List(10) 

val t3 = eval(List(Push(5), Inc, Inc, Push(1), Pop))
println(s"Test 3: $t3") // List(7)

val t4 = eval(List())
println(s"Test 4: $t4") // List()

val t5 = eval(List(Pop, Push(1)))
println(s"Test 5: $t5 ") // List(1)