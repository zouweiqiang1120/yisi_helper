import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const YisiHelperApp());
}

class YisiHelperApp extends StatelessWidget {
  const YisiHelperApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '易思培训助手',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
