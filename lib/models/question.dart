class Question {
  final int? id;
  final String question;
  final String answer;
  final String? optionA;
  final String? optionB;
  final String? optionC;
  final String? optionD;
  final String? type;

  Question({
    this.id,
    required this.question,
    required this.answer,
    this.optionA,
    this.optionB,
    this.optionC,
    this.optionD,
    this.type,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'question': question,
      'answer': answer,
      'optionA': optionA,
      'optionB': optionB,
      'optionC': optionC,
      'optionD': optionD,
      'type': type,
    };
  }

  factory Question.fromMap(Map<String, dynamic> map) {
    return Question(
      id: map['id'],
      question: map['question'],
      answer: map['answer'],
      optionA: map['optionA'],
      optionB: map['optionB'],
      optionC: map['optionC'],
      optionD: map['optionD'],
      type: map['type'],
    );
  }
}
