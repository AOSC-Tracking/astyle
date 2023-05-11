#compdef astyle

_astyle() {
  local -a options=(
    "--style[Set a formatting and indenting style]: :(allman java kr stroustrup whitesmith vtk ratliff gnu linux horstmann 1tbs google mozilla webkit pico lisp)"
    "--indent[Set indentation option]: :(spaces tab force-tab force-tab-x)"
    "--attach-namespaces[Attach braces to a namespace statement]"
    "--attach-classes[Attach braces to a class statement]"
    "--attach-inlines[Attach braces to class inline function definitions]"
    "--attach-extern-c[Attach braces to an extern C statement]"
    "--attach-closing-while[Attach closing while of do-while to the closing brace]"
    "--indent-classes[Indent 'class' blocks so that the entire block is indented]"
    "--indent-modifiers[Indent 'class' access modifiers, 'public\:', 'protected\:' or 'private\:', one half indent]"
    "--indent-switches[Indent 'switch' blocks, so that the inner 'case XXX\:'  headers are indented in relation to the switch block]"
    "--indent-cases[Indent case blocks from the 'case XXX\:' headers]"
    "--indent-namespaces[Indent the contents of namespace blocks]"
    "--indent-after-parens[Indent, instead of align, continuation lines following lines that contain an opening paren '(' or an assignment '=']"
    "--indent-continuation[Indent continuation lines an additional indents]: :(0 1 2 3 4)"
    "--indent-labels[Indent labels so that they appear one indent less than the current indentation level, rather than being flushed completely to the left]"
    "--indent-preproc-block[Indent preprocessor blocks at brace level 0]"
    "--indent-preproc-cond[Indent preprocessor conditional statements #if/#else/#endif to the same level as the source code]"
    "--indent-preproc-define[Indent multi-line preprocessor #define statements]"
    "--indent-col1-comments[Indent line comments that start in column one]"
    "--min-conditional-indent[Indent a minimal # spaces in a continuous conditional belonging to a conditional header]: :(0 1 2 3)"
    "--max-continuation-indent[Indent a maximal # spaces in a continuation line, relative to the previous line]: :_files"
    "--break-blocks[Insert empty lines around unrelated blocks, labels, classes, ..]: :(all)"
    "--pad-oper[Insert space padding around operators]"
    "--pad-comma[Insert space padding after commas]"
    "--pad-paren[Insert space padding around parenthesis on both the outside and the inside]"
    "--pad-paren-out[Insert space padding around parenthesis on the outside only]"
    "--pad-first-paren-out[Insert space padding around first parenthesis in a series on the outside only]"
    "--pad-paren-in[Insert space padding around parenthesis on the inside only]"
    "--pad-header[Insert space padding after paren headers (e.g]"
    "--unpad-paren[Remove unnecessary space padding around parenthesis]"
    "--pad-brackets[Insert space padding around square brackets on both the outside and the inside (experimental)]"
    "--unpad-brackets[Remove unnecessary space padding around square brackets (experimental)]"
    "--delete-empty-lines[Delete empty lines within a function or method]"
    "--fill-empty-lines[Fill empty lines with the white space of their previous lines]"
    "--align-pointer[Attach a pointer or reference operator (*, &, or ^) to either the operator type (left), middle, or operator name (right)]: :(type middle name)"
    "--align-reference[Attach a reference operator (&) to either the operator type (left), middle, or operator name (right)]: :(none type middle name)"
    "--break-closing-braces[Break braces before closing headers (e.g]"
    "--break-elseifs[Break 'else if()' statements into two different lines]"
    "--break-one-line-headers[Break one line headers (e.g]"
    "--add-braces[Add braces to unbraced one line conditional statements]"
    "--add-one-line-braces[Add one line braces to unbraced one line conditional statements]"
    "--remove-braces[Remove braces from a braced one line conditional statements]"
    "--break-return-type[Break the return type from the function name definitions]"
    "--attach-return-type-decl[Break the return type from the function name declarations]"
    "--keep-one-line-blocks[Don't break blocks residing completely on one line]"
    "--keep-one-line-statements[Don't break lines containing multiple statements into multiple single-statement lines]"
    "--convert-tabs[Convert tabs to the appropriate number of spaces]"
    "--close-templates[Close ending angle brackets on template definitions]"
    "--remove-comment-prefix[Remove the leading '*' prefix on multi-line comments and indent the comment text one indent]"
    "--max-code-length[Break the line if it exceeds more than # characters]: :_files"
    "--break-after-logical[After break line using --max-code-length, place logical conditional last on the previous line]"
    "mode[Set input syntax mode]: :(c java cs objc js)"
    "--pad-method-prefix[Insert space padding after the '-' or '+' Objective-C method prefix]"
    "--unpad-method-prefix[Remove all space padding after the '-' or '+' Objective-C method prefix]"
    "--pad-return-type[Insert space padding after the Objective-C return type]"
    "--unpad-return-type[Remove all space padding after the Objective-C return type]"
    "--pad-param-type[Insert space padding after the Objective-C param type]"
    "--unpad-param-type[Remove all space padding after the Objective-C param type]"
    "--align-method-colon[Align the colons in an Objective-C method definition]"
    "--pad-method-colon[Add or remove space padding before or after the colons in an Objective-C method call]: :(none all after before)"
    "--suffix[Append the suffix #### instead of '.orig' to original filename or do not retain a backup of the original file if set to none]: :_files"
    "--recursive[Process subdirectories recursively]"
    "--dry-run[Perform a trial run with no changes made to check for formatting]"
    "--exclude[Specify a file or directory #### to be excluded from processing]: :_files"
    "--ignore-exclude-errors[Allow processing to continue if there are errors in the --exclude options]"
    "--ignore-exclude-errors-x[Allow processing to continue if there are errors in the --exclude options]"
    "--errors-to-stdout[Print errors and help information to standard-output rather than to standard-error]"
    "--preserve-date[Preserve the original file's date and time modified]"
    "--verbose[Extra informational messages will be displayed]"
    "--formatted[Display only the files that have been formatted]"
    "--quiet[Suppress all output except error messages]"
    "--lineend[Force use of the specified line end style]: :(windows linux macold)"
    "--options[Specify a default option file to read and use]: :_files"
    "--project[Specify a project option file to read and use]: :_files"
    "--ascii[The displayed output will be ASCII characters only]"
    "--version[Print version number]"
    "--help[Print help message]"
    "--html[Open the HTML help file astyle.html in the default browser]"
    "--stdin[Use the file path as input to single file formatting]: :_files"
    "--stdout[Use the file path as output from single file formatting]: :_files"
    "--squeeze-lines[Remove superfluous empty lines exceeding the given number]: :_files"
    "--squeeze-ws[Remove superfluous whitespace]"
  )
  _arguments -s -S \
    $options \
    "*: :_files" \
    && return 0

  return 1
}

_astyle
