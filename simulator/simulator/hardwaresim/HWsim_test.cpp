**** function
****** defun: define function的语法, 不需要 progn
[[/Users/quebec/Documents/Book/An Introduction to Programming in Emacs
Lisp by Robert J. Chassell (z-lib.pdf#:47]]

举个最简单的例子:

#+begin_example
(defun hello (name) (insert "Hello " name))
#+end_example

A function definition has up to five parts following the word defun: 1.
The name of the symbol to which the function definition should be
attached. 2. A list of the arguments that will be passed to the
function. If no argu­ ments will be passed to the function, this is an
empty list, (). 3. Documentation describing the function. (Technically
optional, but strongly recommended.) 4. Optionally, an expression to
make the function interactive so you can use it by typing M-x and then
the name of the function; or by typing an appropriate key or
keychord. 5. The code that instructs the computer what to do: the body
of the function definition.

#+begin_example
(defun function-name (arguments...)
"optional-documentation.. . "
(interactive argument-passing-info) ;
optional body...)
#+end_example
****** function 本身并不是 symbol, 不过需要 function 作为参数, 通常是 lambda 或者 symbol
#+begin_src emacs-lisp :tangle yes
print
#+end_src
这是错误的, 因为 function 并不是 symbol.
****** function有返回值
比如 =(set 'flowers '(rose violet daisy buttercup))= 的返回值就是
=(rose violet daisy buttercup)= .

****** document string(C-h f)
The argument list is followed by the documentation string that describes
the function. This is what you see when you type C-h f and the name of a
function. Incidentally, when you write a documentation string like this,
you should make the first line a complete sentence since some commands,
such as apropos, print only the first line of a multi-line documentation
string.

****** interactive: make command
关于各种参数, 比如
=(interactive "F")= 这个F是什么意思.
见[[https://www.gnu.org/software/emacs/manual/html_node/elisp/Interactive-Codes.html][这个]].
比如F的意义是: A file name. The file need not exist. Completion,
Default, Prompt.

作用: A user can invoke an interactive function by typing M-x and then
the name of the function; or by typing the keys to which it is bound,
for example, by typing C-n for next-line or C-x h for mark-whole-buffer.

如果函数没有参数, 只是为了可以用快捷键或者M-x来使用, 不需要参数,
=(interactie)= 即可.

位置: immediately after the documentation.

when you call an interactive function interactively, the value returned
is not automatically displayed in the echo area.

#+begin_example
(defun multiply-by-seven (number) ; Interactive version.
"Multiply NUMBER by seven."
(interactive "p")
(message "The result is 7,%d" (* 7 number)))
#+end_example

怎么传参数? 先C-u, 再3, 再M-x, 再输入multiply-by-seven. 或者M-3 M-x
multiply-by-seven 这个3, 被称为[[#prefix argument]]

#question 仍然不知道如果为空是什么? 难道是, 可以M-x, 但没有参数?
=(interactive)= 与 =(interative "")= 等价么?

#+begin_src emacs-lisp :tangle yes
(consult-ripgrep)
#+end_src

******* r: region

****** prefix argument
没啥, 就是interactive, 'p'对应的, 在M-x给出函数名之前, 先给出参数.

****** numeric arguments
[[skim:///Users/quebec/Documents/Book/emacs_manual.pdf::50]]

The easiest way to specify a numeric argument is to type a digit and/or a minus sign while holding down the META key. For example,
M-5 C-n
moves down five lines. The keys M-1, M-2, and so on, as well as M--, are bound
to commands (digit-argument and negative-argument) that set up an argument for the next command. Meta-- without digits normally means −1.
If you enter more than one digit, you need not hold down the META key for the second and subsequent digits. Thus, to move down fifty lines, type
M-5 0 C-n, 相当于  50.

Instead of typing M-1, M-2, and so on, another way to specify a numeric argument is to type C-u (universal-argument) followed by some digits, or (for a negative argument) a minus sign followed by digits. A minus sign without digits normally means −1.
C-u alone has the special meaning of “four times”: it multiplies the argument for the next command by four. C-u C-u multiplies it by sixteen. Thus, C-u C-u C-f moves forward sixteen characters. Other useful combinations are C-u C-n, C-u C-u C-n (move down a good fraction of a screen), C-u C-u C-o (make “a lot” of blank lines), and C-u C-k (kill four lines).

You can use a numeric argument before a self-inserting character to insert mul- tiple copies of it. This is straightforward when the character is not a digit; for example, C-u 6 4 a inserts 64 copies of the character ‘a’. But this does not work for inserting digits; C-u 6 4 1 specifies an argument of 641. You can separate the
argument from the digit to insert with another C-u; for example, C-u 6 4 C-u 1 does insert 64 copies of the character ‘1’.
Some commands care whether there is an argument, but ignore its value. For example, the command M-q (fill-paragraph) fills text; with an argument, it jus- tifies the text as well. (See Section 22.5 [Filling], page 218, for more information on M-q.) For these commands, it is enough to the argument with a single C-u.

举个例子:

org-clock-display

With ‘SPC u SPC u’ prefix, use a custom range, entered at prompt.

With ‘SPC u SPC u SPC u’ prefix, display the total time in the
echo area.

****** lambda
举例子:

#+begin_src emacs-lisp :tangle yes
(global-set-key (kbd "s-w") (lambda ()
															(interactive)
															(kill-buffer (current-buffer))))
#+end_src


int main()
{
	//hwsim->SaveOutput("HWoutput");

	return 0;
}
