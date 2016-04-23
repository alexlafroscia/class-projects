/*
 * Dice Driver
 * Alex LaFroscia <alex@lafroscia.com>
 *
 */

#include <linux/fs.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/module.h>
#include <linux/random.h>
#include <asm/uaccess.h>


/*
* Get a randon character using the helper function
* from <linux/random>
*/
unsigned char get_random_byte(int max)
{
  unsigned char c;
  get_random_bytes(&c, 1);
  return c % max;
}


/*
 * dice_driver_read is the function called when a process calls read() on
 * /dev/dice_driver.  It writes a random dice roll to the buffer passed in the
 * read() call.
 */
static ssize_t dice_driver_read(struct file * file, char * buf, size_t count, loff_t *ppos)
{
  unsigned char *dice_driver_str;
  int i, len;

  dice_driver_str = kmalloc(sizeof(unsigned char) * count, GFP_KERNEL);

  for (i = 0; i < count; i++)
  {
    dice_driver_str[i] = get_random_byte(7);
  }

  len = strlen(dice_driver_str); /* Don't include the null byte. */
  /*
   * We only support reading the whole string at once.
   */
  if (count < len)
    return -EINVAL;
  /*
   * If file position is non-zero, then assume the string has
   * been read and indicate there is no more data to be read.
   */
  if (*ppos != 0)
    return 0;
  /*
   * Besides copying the string to the user provided buffer,
   * this function also checks that the user has permission to
   * write to the buffer, that it is mapped, etc.
   */
  if (copy_to_user(buf, dice_driver_str, len))
    return -EINVAL;
  /*
   * Tell the user how much data we wrote.
   */
  *ppos = len;

  kfree(dice_driver_str);
  return len;
}


/*
 * The only file operation we care about is read.
 */

static const struct file_operations dice_driver_fops = {
  .owner		= THIS_MODULE,
  .read		  = dice_driver_read,
};

static struct miscdevice dice_driver_dev = {
  MISC_DYNAMIC_MINOR,
  "dice_driver",
  &dice_driver_fops
};

static int __init
dice_driver_init(void)
{
  int ret;

  /*
   * Create the "dice_driver" device in the /sys/class/misc directory.
   * Udev will automatically create the /dev/dice_driver device using
   * the default rules.
   */
  ret = misc_register(&dice_driver_dev);
  if (ret)
    printk(KERN_ERR
           "Unable to register \"dice driver\" misc device\n");

  return ret;
}

module_init(dice_driver_init);

static void __exit
dice_driver_exit(void)
{
  misc_deregister(&dice_driver_dev);
}

module_exit(dice_driver_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Alex LaFroscia <alex@lafroscia.com>");
MODULE_DESCRIPTION("Get a random dice roll");
MODULE_VERSION("dev");
