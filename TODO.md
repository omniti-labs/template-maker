# Items to do

 * Tests/examples
   * Pick some more sample files
     * postgres config?
 * Additional filters
   * underscore_to_camel
   * uppercase
   * lowercase
 * Detect duplicate keys and make them into lists
   * Example:

        HostKey /etc/ssh/foo.key
        HostKey /etc/ssh/bar.key

  * This should be translated into:

        # Chef
        <% node[:foo][:host_key].each do |i| %>
        HostKey <%= i %>
        <% end %>
        # Ansible
        {% for i in foo_host_key %}
        HostKey {{ i }}
        {% endfor %}

    * Thoughts:
      * This only works if the values are consecutive
      * If they're not, we might need to come up with another option, such
        as naming the vars host_key_1, host_key_2 and so on.
      * We can keep the array for non-consecutive values also:
        * {{ foo_host_key[0] }}
        * {{ foo_host_key[1] }}
        * Perhaps detect if it's consecutive and use the for loop if so, and
          the array method if not.
      * We should provide this as an option on the template command line
      * Maybe actions should have options allowed also:
        * REGEX template camel multi_array # Array method
        * REGEX template multi_suffix # Var suffix method
